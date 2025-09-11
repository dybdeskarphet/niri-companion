from pathlib import Path
from sys import argv
from companion.config import AppConfig, load_config

APP_NAME = "niri-genconfig"


class GenConfig:
    def __init__(self) -> None:
        self.config: AppConfig = load_config()

    def check_files(self):
        non_existent_files: list[str] = []

        for fname in self.config.genconfig.sources:
            if not Path(fname).exists():
                non_existent_files.append(fname)

        if len(non_existent_files) != 0:
            print("Couldn't find the files below, check your genconfig.sources:")
            print(*non_existent_files, sep="\n")
            exit(1)

    def generate(self):
        self.check_files()
        with open(self.config.general.output_path, "w", encoding="utf-8") as outfile:
            for fname in self.config.genconfig.sources:
                with open(fname, "r", encoding="utf-8") as infile:
                    _ = outfile.write(infile.read())
                    _ = outfile.write("\n")
        print(
            f"Generation successful! Output written to: {self.config.general.output_path}"
        )


def main():
    if len(argv) < 2:
        print(f"Usage: {APP_NAME} [generate]")
        return

    mode = argv[1]

    if mode == "generate":
        GenConfig().generate()
    else:
        print("Unknown mode:", mode)
        exit(1)


if __name__ == "__main__":
    main()
