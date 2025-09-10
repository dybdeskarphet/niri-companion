from pathlib import Path
from sys import argv
from companion.config import AppConfig, load_config

APP_NAME = "niri-genconfig"


class GenConfig:
    def __init__(self) -> None:
        self.config: AppConfig = load_config()

    def gen_config(self):
        all_files_found = True

        with open(self.config.general.output_path, "w", encoding="utf-8") as outfile:
            for fname in self.config.genconfig.sources:
                if not Path(fname).exists():
                    print(f"Source file missing: {fname}")
                    all_files_found = False
                    continue
                with open(fname, "r", encoding="utf-8") as infile:
                    _ = outfile.write(infile.read())
                    _ = outfile.write("\n")

        if all_files_found:
            print(
                f"Generation successful! Output written to: {self.config.general.output_path}"
            )
        else:
            print(
                f"Generation completed with missing files. Check logs above. Output written to: {self.config.general.output_path}"
            )


def main():
    if len(argv) < 2:
        print(f"Usage: {APP_NAME} [generate]")
        return

    mode = argv[1]

    if mode == "generate":
        GenConfig().gen_config()
    else:
        print("Unknown mode:", mode)
        exit(1)


if __name__ == "__main__":
    main()
