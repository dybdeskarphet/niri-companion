# Niri Companion

**Niri Companion** is a toolkit that adds extra functionality to [niri](https://github.com/YaLTeR/niri).

## Installation

Install with `pipx` or `pip` accordingly:

```
pipx install niri-companion
pip install niri-companion
```

## Configuration

The configuration file is located at:

```
~/.config/niri-companion/settings.toml
```

Check out the [example configuration file](./examples/settings.toml) for reference.

## Tools

### `niri-genconfig`

Generates a `config.kdl` by concatenating files from a specified directory.
This lets you split your configuration into smaller, more manageable pieces.

### `niri-ipcext`

> [!WARNING]
> `niri-ipcext` does not use a proper KDL parser/writer. Instead, it relies on a custom workaround described below, which can be brittle in some cases.

Edits `config.kdl` by replacing `old_text` with `new_text`.
To revert the changes, run `niri-genconfig generate`.
This provides IPC-like behavior, similar to Hyprland's IPC.

### `niri-workspaces`

Lets you define workflows that automatically launch specific programs on specific workspaces.
For example: open your browser on workspace 1 and your editor on workspace 2.

## Important Notes

The `config.kdl` file should be treated as **temporary**:

* `niri-genconfig` will overwrite it when generating configs.
* `niri-ipcext` depends on `config.kdl` being updated dynamically.

If you want a permanent configuration, keep it in separate files and let `niri-genconfig` handle the final `config.kdl`.
