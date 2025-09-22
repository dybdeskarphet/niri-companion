from pathlib import Path
from sys import argv
import threading
import time
from typing import override
from companion.config import AppConfig, load_config
from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler
from companion.utils import Logger
import typer
from typing_extensions import Annotated

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

        for source in self.config.genconfig.sources:
            if isinstance(source, str):
                if not Path(source).exists():
                    non_existent_files.append(source)
            else:
                for source_array_item in source:
                    if not Path(source_array_item.path).exists():
                        non_existent_files.append(source_array_item.path)

        if len(non_existent_files) != 0:
            logger.print("Couldn't find the files below, check your genconfig.sources:")
            print(*non_existent_files, sep="\n")
            exit(1)

    def generate(self, mode: str = "default"):
        with open(self.config.general.output_path, "w", encoding="utf-8") as outfile:
            for source in self.config.genconfig.sources:
                if isinstance(source, str):
                    with open(source, "r", encoding="utf-8") as infile:
                        _ = outfile.write(infile.read())
                        _ = outfile.write("\n")
                else:
                    for source_array_item in source:
                        if source_array_item.group == mode:
                            with open(
                                source_array_item.path, "r", encoding="utf-8"
                            ) as infile:
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


app = typer.Typer(
    help="niri-companion config generation tool",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command(help="Generate configuration")
def generate(group: Annotated[str, typer.Argument()] = "default"):
    gen = GenConfig()
    gen.check_files()
    gen.generate(group)


@app.command(help="Start config generation daemon")
def dameon():
    gen = GenConfig()
    gen.check_files()
    gen.daemon()


if __name__ == "__main__":
    app()
