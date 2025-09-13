from os import environ, path
from pydantic import BaseModel, RootModel, ValidationError
from pathlib import Path
import tomllib
from sys import exit

from companion.utils import ConfigPath, Logger


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
        logger.error(f"Config file not found: {companion_settings_path}")
        exit(1)
    except tomllib.TOMLDecodeError as e:
        logger.error(f"Failed to parse TOML: {e}")
        exit(1)
    except ValidationError as e:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table()
        table.add_column("Location", style="cyan")
        table.add_column("Message", style="red")
        table.add_column("Type", style="magenta")

        for err in e.errors():
            loc = " -> ".join(str(x) for x in err["loc"])
            table.add_row(loc, err["msg"], err["type"])

        logger.error(f"Invalid config file:")
        console.print(table)
        exit(1)

    for i, s in enumerate(config.genconfig.sources):
        config.genconfig.sources[i] = path.expanduser(path.expandvars(s))

    config.genconfig.watch_dir = path.expanduser(
        path.expandvars(config.genconfig.watch_dir)
    )

    if not Path(config.genconfig.watch_dir).exists():
        logger.error("Watch directory doesn't exist, check your genconfig.watch_dir:")
        exit(1)

    config.general.output_path = path.expanduser(
        path.expandvars(str(config.general.output_path))
    )

    config.workspaces.dmenu_command = path.expandvars(
        config.workspaces.dmenu_command
    ).replace("~", str(Path.home()))

    return config
