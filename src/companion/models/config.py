from pydantic import BaseModel, RootModel


class ConfigItem(BaseModel):
    group: str
    path: str


class GeneralConfig(BaseModel):
    output_path: str


class GenConfigSection(BaseModel):
    sources: list[str | list[ConfigItem]]
    watch_dir: str = "~/.config/niri/soruces"


class WorkspaceItem(BaseModel):
    workspace: int
    run: str
    task_delay: float | None = None


class WorkspaceItemsSection(RootModel[dict[str, list[WorkspaceItem]]]):
    def __getitem__(self, item: str) -> list[WorkspaceItem]:
        return self.root[item]


class WorkspaceConfigSection(BaseModel):
    items: WorkspaceItemsSection
    dmenu_command: str = "rofi -dmenu"
    task_delay: float = 0.8


class AppConfig(BaseModel):
    workspaces: WorkspaceConfigSection
    general: GeneralConfig
    genconfig: GenConfigSection
