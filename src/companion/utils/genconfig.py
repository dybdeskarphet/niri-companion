from companion.models.config import ConfigItem
from companion.utils.logger import error


def return_source(source: str | list[ConfigItem], group: str):
    if isinstance(source, str):
        return source
    else:
        for source_array_item in source:
            if source_array_item.group == group:
                return source_array_item.path
            else:
                continue

    error(
        f"The '{group}' group could not be found, or the group defined in one array is not defined in the other arrays."
    )
    exit(1)
