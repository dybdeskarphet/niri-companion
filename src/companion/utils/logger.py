from rich.console import Console

console = Console()


def error(msg: str):
    console.print(rf"[bold red]\[niri-companion][/bold red] {msg}")


def log(msg: str):
    console.print(rf"[bold green]\[niri-companion][/bold green] {msg}")


def warn(msg: str):
    console.print(rf"[bold yellow]\[niri-companion][/bold yellow] {msg}")
