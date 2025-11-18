from pathlib import Path
import threading
import time
from typing import Annotated, override
import typer
from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler
from companion.config import config
from companion.utils.genconfig import return_source
from companion.utils.logger import log, warn


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, gen_config: "GenConfig"):
        self.gen_config: GenConfig = gen_config
        self.timer = None

    @override
    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent):
        if event.is_directory:
            return
        log(f"{event.src_path} changed, regenerating...")
        if self.timer:
            self.timer.cancel()
        # NOTE: Modern editors don't do in-place editing, instead they
        # use a temp file and replace the old file with the new file. watchdog
        # is really fast so this behaviour makes it think that file doesn't
        # exist for a moment and throws errors. 0.4 enough even for older hardware.
        self.timer = threading.Timer(0.4, self.gen_config.generate)
        self.timer.start()


class GenConfig:
    def __init__(self, group: str = "default") -> None:
        self.group: str = group

    def check_files(self):
        non_existent_files: list[str] = []

        for source in config.genconfig.sources:
            parsed_source_path = return_source(source, self.group)
            if not Path(parsed_source_path).exists():
                non_existent_files.append(parsed_source_path)

        if len(non_existent_files) != 0:
            warn("Couldn't find the files below, check your genconfig.sources:")
            print(*non_existent_files, sep="\n")
            exit(1)

    def generate(self):
        with open(config.general.output_path, "w", encoding="utf-8") as outfile:
            for source in config.genconfig.sources:
                parsed_source_path = return_source(
                    source,
                    self.group,
                )
                with open(parsed_source_path, "r", encoding="utf-8") as infile:
                    _ = outfile.write(infile.read())
                    _ = outfile.write("\n")

        log(f"Generation successful! Output written to: {config.general.output_path}")

    def daemon(self):
        from watchdog.observers import Observer

        self.generate()
        observer = Observer()
        handler = FileChangeHandler(self)
        _ = observer.schedule(handler, config.genconfig.watch_dir)
        observer.start()
        log(
            f"Watching {config.genconfig.watch_dir} for changes, press [yellow]Ctrl+C[/yellow] to stop the daemon."
        )

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            log("Killing the daemon, goodbye!")
            observer.stop()
        observer.join()


app = typer.Typer(
    help="niri-companion config generation tool",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command(help="Generate configuration")
def generate(group: Annotated[str, typer.Argument()] = "default"):
    gen = GenConfig(group)
    gen.check_files()
    gen.generate()


@app.command(help="Start config generation daemon")
def daemon(group: Annotated[str, typer.Argument()] = "default"):
    gen = GenConfig(group)
    gen.check_files()
    gen.daemon()


if __name__ == "__main__":
    app()
