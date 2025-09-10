from sys import argv
from companion.genconfig import GenConfig
from companion.config import AppConfig, load_config

APP_NAME = "niri-ipcext"


class IpcExt:
    def __init__(self) -> None:
        self.config: AppConfig = load_config()

    def restore(self):
        GenConfig().gen_config()

    def replace_line(self, old: str, new: str):

        with open(self.config.general.output_path, "r") as f:
            lines = f.readlines()

        matching_lines = [i for i, line in enumerate(lines) if old in line]

        if len(matching_lines) == 0:
            print("No matching line found.")
            return False
        elif len(matching_lines) > 1:
            print("Error: More than one matching line found.")
            return False

        index = matching_lines[0]
        lines[index] = new + "\n"

        with open(self.config.general.output_path, "w") as f:
            f.writelines(lines)

        return True


def main():
    if len(argv) < 2:
        print(f"Usage: {APP_NAME} [replace|restore] <grep_text> <new_text>")
        return

    mode = argv[1]

    if mode == "replace":
        old, new = argv[2], argv[3]
        res = IpcExt().replace_line(old, new)
        if res:
            print("ok")
            exit(0)
    elif mode == "restore":
        res = IpcExt().restore()
        print("ok")
        exit(0)
    else:
        print("Unknown mode:", mode)
        exit(1)


if __name__ == "__main__":
    main()
