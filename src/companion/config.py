from os import environ
from pathlib import Path
import tomllib
from companion.models.config import (
    AppConfig,
    ConfigItem,
    GenConfigSection,
    GeneralConfig,
    WorkspaceConfigSection,
    WorkspaceItem,
    WorkspaceItemsSection,
)
from companion.utils.general import expandall
import tomli_w
from pydantic import ValidationError
from companion.utils.logger import console, error, log, warn


class ConfigPath:
    dir: Path

    def __init__(self, program: str) -> None:
        home = environ.get("HOME")
        xdg_config = environ.get("XDG_CONFIG_HOME")

        if home:
            if xdg_config:
                self.dir = Path(xdg_config) / program
            else:
                self.dir = Path(home) / ".config" / program
        else:
            error("No home directory found.")

    # TODO: Typo, make it create_dir
    def create_dir(self):
        self.dir.mkdir(parents=True, exist_ok=True)


companion_config = ConfigPath("niri-companion")
companion_config.create_dir()
COMPANION_SETTINGS_PATH = companion_config.dir / "settings.toml"


def create_empty_config(path: Path):
    empty_config = AppConfig(
        general=GeneralConfig(output_path="~/.config/niri/probably_config.kdl"),
        workspaces=WorkspaceConfigSection(
            dmenu_command="rofi -dmenu",
            task_delay=0.8,
            items=WorkspaceItemsSection(
                {"example": [WorkspaceItem(workspace=1, run="brave")]}
            ),
        ),
        genconfig=GenConfigSection(
            sources=[
                "~/.config/niri/sources/first_config.kdl",
                "~/.config/niri/sources/second_config.kdl",
                [
                    ConfigItem(
                        group="default",
                        path="~/.config/niri/sources/default_visuals.kdl",
                    ),
                    ConfigItem(
                        group="custom",
                        path="~/.config/niri/sources/custom_visuals.kdl",
                    ),
                ],
            ],
            watch_dir="~/.config/niri/sources/",
        ),
    )

    try:
        with open(str(path), "wb") as f:
            tomli_w.dump(empty_config.model_dump(), f)
        log("Config file created successfully!")
        warn(
            "Please edit the configuration file. Default configurations serve as placeholders."
        )
    except PermissionError:
        error("No permission to write this file :/")


def read_config_file():
    try:
        with open(COMPANION_SETTINGS_PATH, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        from rich.prompt import Confirm

        error(f"Config file not found at {COMPANION_SETTINGS_PATH}")
        ans = Confirm.ask("Do you want to create a new configuration file?")
        if ans:
            create_empty_config(COMPANION_SETTINGS_PATH)
        exit(1)
    except tomllib.TOMLDecodeError as e:
        error(f"Failed to parse TOML: {e}")
        exit(1)


def expand_config(config: AppConfig):
    for i, s in enumerate(config.genconfig.sources):
        if isinstance(s, list):
            for item in s:
                item.path = expandall(item.path)
        else:
            config.genconfig.sources[i] = expandall(s)

    config.genconfig.watch_dir = expandall(config.genconfig.watch_dir)

    if not Path(config.genconfig.watch_dir).exists():
        error("Watch directory doesn't exist, check your genconfig.watch_dir:")
        exit(1)

    config.general.output_path = expandall(config.general.output_path)
    config.workspaces.dmenu_command = expandall(config.workspaces.dmenu_command)


def load_config():
    try:
        with open(COMPANION_SETTINGS_PATH, "rb") as f:
            raw = read_config_file()
            config = AppConfig(**raw)
    except ValidationError as e:
        from rich.table import Table
        from rich import box

        table = Table("Location", "Message", "Type", box=box.ROUNDED, min_width=80)
        for err in e.errors():
            loc = " -> ".join(str(x) for x in err["loc"])
            table.add_row(loc, err["msg"], err["type"])

        error(f"Invalid config file:")
        console.print(table)
        exit(1)

    expand_config(config)

    return config


config = load_config()
