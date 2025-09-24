from typing import Annotated
import typer
from companion.config import config
from companion.genconfig import GenConfig
from companion.utils.logger import console, log


class IpcExt:
    def __init__(self) -> None:
        pass

    def restore(self):
        GenConfig().generate()

    def replace_line(self, old: str, new: str):
        with open(config.general.output_path, "r") as f:
            lines = f.readlines()

        matching_lines = [i for i, line in enumerate(lines) if old in line]

        if len(matching_lines) == 0:
            console.print("No matching line found.")
            return False
        elif len(matching_lines) > 1:
            console.print("Error: More than one matching line found.")
            return False

        index = matching_lines[0]
        lines[index] = new + "\n"

        with open(config.general.output_path, "w") as f:
            f.writelines(lines)

        return True


app = typer.Typer(
    help="niri-companion IPC-like configuration tool",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command(help="Replace string inside niri configuration file")
def replace(
    old: Annotated[str, typer.Argument()], new: Annotated[str, typer.Argument()]
):
    res = IpcExt().replace_line(old, new)
    if res:
        log("Done!")
        exit(0)


@app.command(help="Restore default settings")
def restore():
    res = IpcExt().restore()
    log("Done!")
    exit(0)


if __name__ == "__main__":
    app()
