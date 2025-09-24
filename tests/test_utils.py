import os
from pathlib import Path
import pytest

from companion.models.config import ConfigItem
from companion.utils.genconfig import return_source
from companion.utils.general import expandall


def test_expandall():
    os.environ["HOME"] = "/home/testing"
    home = os.environ["HOME"]
    assert expandall("~/.config/niri") == str(Path(home) / ".config" / "niri")
    assert expandall("$HOME/.config/niri") == str(Path(home) / ".config" / "niri")
    assert (
        expandall("This is a ~/.config/niri sentence.")
        == "This is a " + str(Path(home) / ".config" / "niri") + " sentence."
    )


def test_source_array():
    config_items = [
        ConfigItem(group="default", path="somewhere"),
        ConfigItem(group="cool", path="someone"),
    ]

    assert return_source(config_items, "default") == "somewhere"
    assert return_source(config_items, "cool") == "someone"
    assert return_source("hey", "default") == "hey"
    assert return_source("hey", "invalid group") == "hey"
