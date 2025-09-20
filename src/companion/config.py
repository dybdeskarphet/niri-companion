from pydantic import BaseModel, RootModel, ValidationError
from pathlib import Path
import tomllib
from sys import exit
import tomli_w

from companion.utils import ConfigPath, Logger, expandall


class GeneralConfig(BaseModel):
    output_path: str


class GenConfigSection(BaseModel):
    sources: list[str]
    watch_dir: str


class WorkspaceItem(BaseModel):
    workspace: int
    run: str


class WorkspaceItemsSection(RootModel[dict[str, list[WorkspaceItem]]]):
    def __getitem__(self, item: str) -> list[WorkspaceItem]:
        return self.root[item]


class WorkspaceConfigSection(BaseModel):
    items: WorkspaceItemsSection
    dmenu_command: str
    task_delay: float


class AppConfig(BaseModel):
    workspaces: WorkspaceConfigSection
    general: GeneralConfig
    genconfig: GenConfigSection


def create_empty_config(logger: Logger, path: Path):
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
            ],
            watch_dir="~/.config/niri/sources/",
        ),
    )

    try:
        with open(str(path), "wb") as f:
            tomli_w.dump(empty_config.model_dump(), f)
        logger.print("Config file created successfully!")
        logger.warn(
            "Please edit the configuration file, otherwise the niri-genconfig command may reset your existing niri configuration file."
        )
    except PermissionError:
        logger.error("No permission to write this file :/")


def load_config():

    APP_NAME = "niri-companion|config"
    logger = Logger(f"[{APP_NAME}]")

    companion_config = ConfigPath("niri-companion")
    companion_config.creat_dir()
    companion_settings_path = companion_config.dir / "settings.toml"

    try:
        with open(companion_settings_path, "rb") as f:
            raw = tomllib.load(f)
            config = AppConfig(**raw)
    except FileNotFoundError:
        from rich.prompt import Confirm

        logger.error(f"Config file not found at {companion_settings_path}")
        ans = Confirm.ask("Do you want to create a new configuration file?")
        if ans:
            create_empty_config(logger, companion_settings_path)
        exit(1)
    except tomllib.TOMLDecodeError as e:
        logger.error(f"Failed to parse TOML: {e}")
        exit(1)
    except ValidationError as e:
        from rich.console import Console
        from rich.table import Table
        from rich import box

        console = Console()
        table = Table("Location", "Message", "Type", box=box.ROUNDED, min_width=80)
        for err in e.errors():
            loc = " -> ".join(str(x) for x in err["loc"])
            table.add_row(loc, err["msg"], err["type"])

        logger.error(f"Invalid config file:")
        console.print(table)
        exit(1)

    for i, s in enumerate(config.genconfig.sources):
        config.genconfig.sources[i] = expandall(s)

    config.genconfig.watch_dir = expandall(config.genconfig.watch_dir)

    if not Path(config.genconfig.watch_dir).exists():
        logger.error("Watch directory doesn't exist, check your genconfig.watch_dir:")
        exit(1)

    config.general.output_path = expandall(str(config.general.output_path))
    config.workspaces.dmenu_command = expandall(config.workspaces.dmenu_command)

    return config
