class Logger:
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def print(self, msg: str) -> None:
        print(f"\033[32m{self.prefix}\033[0m {msg}")

    def error(self, msg: str) -> None:
        print(f"\033[31m{self.prefix}\033[0m {msg}")
