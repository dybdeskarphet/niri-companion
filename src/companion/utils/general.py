from os import path
from pathlib import Path


def expandall(p: str):
    if p.startswith("~"):
        return path.expanduser(path.expandvars(p))
    else:
        return path.expandvars(p).replace("~", str(Path.home()))
