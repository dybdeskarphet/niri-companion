from pydantic import BaseModel, RootModel


class ConfigItem(BaseModel):
    group: str
    path: str


class GeneralConfig(BaseModel):
    output_path: str


class GenConfigSection(BaseModel):
    sources: list[str | list[ConfigItem]]
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
