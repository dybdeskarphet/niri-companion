import subprocess
import time
from companion.config import load_config


def main():
    config = load_config()
    workspace_strings = list(config.workspaces.items.root.keys())
    menu = "\n".join(workspace_strings)

    try:
        result = subprocess.run(
            config.workspaces.dmenu_command,
            input=menu,
            shell=True,
            text=True,
            capture_output=True,
        )
        choice = result.stdout.strip()
        if choice:
            print("You picked:", choice)
    except Exception as e:
        print("Error:", e)
        exit(1)

    for item in config.workspaces.items.root[choice]:
        ws = item.workspace
        command = item.run

        _ = subprocess.run(f"niri msg action focus-workspace {str(ws)}", shell=True)
        time.sleep(config.workspaces.task_delay)
        _ = subprocess.run(f"niri msg action spawn-sh -- '{command}'", shell=True)
        time.sleep(config.workspaces.task_delay)
        _ = subprocess.run(f"niri msg action maximize-column", shell=True)
        time.sleep(config.workspaces.task_delay)


if __name__ == "__main__":
    main()
