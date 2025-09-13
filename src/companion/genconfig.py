from pathlib import Path
from sys import argv
import threading
import time
from typing import override
from companion.config import AppConfig, load_config
from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler
from companion.utils import Logger

APP_NAME = "niri-genconfig"
logger = Logger(f"[{APP_NAME}]")


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, gen_config: "GenConfig"):
        self.gen_config: GenConfig = gen_config
        self.timer = None

    @override
    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent):
        if event.is_directory:
            return
        logger.print(f"{event.src_path} changed, regenerating...")
        if self.timer:
            self.timer.cancel()
        # NOTE: Modern editors don't do in-place editing, instead they
        # use a temp file and replace the old file with the new file. watchdog
        # is really fast so this behaviour makes it think that file doesn't
        # exist for a moment and throws errors. 0.4 enough even for older hardware.
        self.timer = threading.Timer(0.4, self.gen_config.generate)
        self.timer.start()


class GenConfig:
    def __init__(self) -> None:
        self.config: AppConfig = load_config()

    def check_files(self):
        non_existent_files: list[str] = []

        for fname in self.config.genconfig.sources:
            if not Path(fname).exists():
                non_existent_files.append(fname)

        if len(non_existent_files) != 0:
            logger.print("Couldn't find the files below, check your genconfig.sources:")
            print(*non_existent_files, sep="\n")
            exit(1)

    def generate(self):
        with open(self.config.general.output_path, "w", encoding="utf-8") as outfile:
            for fname in self.config.genconfig.sources:
                with open(fname, "r", encoding="utf-8") as infile:
                    _ = outfile.write(infile.read())
                    _ = outfile.write("\n")
        logger.print(
            f"Generation successful! Output written to: {self.config.general.output_path}"
        )

    def daemon(self):
        from watchdog.observers import Observer

        observer = Observer()
        handler = FileChangeHandler(self)
        watch_dir = self.config.genconfig.watch_dir
        _ = observer.schedule(handler, watch_dir)
        observer.start()
        logger.print(
            f"Watching {watch_dir} for changes, press \033[31mCtrl+C\033[0m to stop the daemon."
        )

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.print("Killing the daemon, goodbye!")
            observer.stop()
        observer.join()


def main():
    if len(argv) < 2:
        print(f"\033[32mUsage:\033[0m {APP_NAME} [generate|daemon]")
        return

    mode = argv[1]

    if mode == "generate":
        gen = GenConfig()
        gen.check_files()
        gen.generate()
    elif mode == "daemon":
        gen = GenConfig()
        gen.check_files()
        gen.daemon()
    else:
        print("\033[31mUnknown mode:\033[0m", mode)
        exit(1)


if __name__ == "__main__":
    main()
