from os import environ, path
from pydantic import BaseModel, RootModel, ValidationError
from pathlib import Path
import tomllib


class GeneralConfig(BaseModel):
    output_path: str


class GenConfigSection(BaseModel):
    sources: list[str]


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
    home = environ.get("HOME")
    xdg_config = environ.get("XDG_CONFIG_HOME")

    if home:
        if xdg_config:
            niri_companion_config_dir = Path(xdg_config) / "niri-companion"
        else:
            niri_companion_config_dir = Path(home) / ".config" / "niri-companion"
    else:
        print("No home directory found.")
        exit(1)

    companion_settings_path = niri_companion_config_dir / "settings.toml"
    niri_companion_config_dir.mkdir(parents=True, exist_ok=True)

    try:
        with open(companion_settings_path, "rb") as f:
            raw = tomllib.load(f)
            config = AppConfig(**raw)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {companion_settings_path}")
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Failed to parse TOML: {e}")
    except ValidationError as e:
        raise ValueError(f"Config validation error: {e}")

    for i, s in enumerate(config.genconfig.sources):
        config.genconfig.sources[i] = path.expanduser(path.expandvars(s))

    config.general.output_path = path.expanduser(
        path.expandvars(str(config.general.output_path))
    )

    config.workspaces.dmenu_command = path.expandvars(
        config.workspaces.dmenu_command
    ).replace("~", str(Path.home()))

    return config
