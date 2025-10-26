import subprocess
import time
from companion.config import config
from companion.utils.logger import error, log


def main():
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
            log(f"You picked: {choice}")
        else:
            error(f"You didn't pick anything")
            exit(1)
    except Exception as e:
        print("Error:", e)
        exit(1)

    for item in config.workspaces.items.root[choice]:
        ws = item.workspace
        command = item.run
        task_delay = item.task_delay

        _ = subprocess.run(f"niri msg action focus-workspace {str(ws)}", shell=True)
        time.sleep(0.3)
        _ = subprocess.run(f"niri msg action spawn-sh -- '{command}'", shell=True)
        if task_delay is not None:
            time.sleep(task_delay)
        else:
            time.sleep(config.workspaces.task_delay)
        _ = subprocess.run(f"niri msg action maximize-column", shell=True)
        time.sleep(0.2)


if __name__ == "__main__":
    main()
