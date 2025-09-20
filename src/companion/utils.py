from os import environ, path
from pathlib import Path


class Logger:
    def __init__(self, prefix: str) -> None:
        self.prefix: str = prefix

    def print(self, msg: str) -> None:
        print(f"\033[32m{self.prefix}\033[0m {msg}")

    def error(self, msg: str) -> None:
        print(f"\033[31m{self.prefix}\033[0m {msg}")

    def warn(self, msg: str) -> None:
        print(f"\033[33m{self.prefix}\033[0m {msg}")


class ConfigPath:
    dir: Path

    def __init__(self, program: str) -> None:
        logger = Logger("[niri-companion|config]")
        home = environ.get("HOME")
        xdg_config = environ.get("XDG_CONFIG_HOME")

        if home:
            if xdg_config:
                self.dir = Path(xdg_config) / program
            else:
                self.dir = Path(home) / ".config" / program
        else:
            logger.error("No home directory found.")
            exit(1)

    def creat_dir(self):
        self.dir.mkdir(parents=True, exist_ok=True)


def expandall(p: str):
    if p.startswith("~"):
        return path.expanduser(path.expandvars(p))
    else:
        return path.expandvars(p).replace("~", str(Path.home()))
