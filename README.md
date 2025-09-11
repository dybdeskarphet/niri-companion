# 🫂 niri-companion

![PyPI - Downloads](https://img.shields.io/pypi/dd/niri-companion) ![PyPI - Version](https://img.shields.io/pypi/v/niri-companion)

**niri-companion** is a toolkit that adds extra functionality to [niri](https://github.com/YaLTeR/niri). See the [CHANGELOG](./CHANGELOG.md) for a detailed list of updates.

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

- `niri-genconfig generate`: Generates an output file (`general.output_path`) by conconcatenating sources (`genconfig.sources`)
- `niri-genconfig daemon`: Same things as above, but auto-generates if files inside the watch directory (`genconfig.watch_dir`) have changed. Works as a daemon.

### `niri-ipcext`

> [!WARNING]
> `niri-ipcext` does not use a proper KDL parser/writer. Instead, it relies on a custom workaround described below, which can be brittle in some cases.

- `niri-ipcext replace`: Edits `config.kdl` by replacing `old_text` with `new_text`.
- `niri-ipcext restore`: Reverts the changes by running `niri-genconfig generate`.

This provides IPC-like behavior, similar to Hyprland's IPC.

### `niri-workspaces`

- Lets you define workflows that automatically launch specific programs on specific workspaces. For example: open your browser on workspace 1 and your editor on workspace 2.
- Needs **rofi** or any program that has a **dmenu functionality**

## Important Notes

The `config.kdl` file should be treated as **temporary**:

* `niri-genconfig` will overwrite it when generating configs.
* `niri-ipcext` depends on `config.kdl` being updated dynamically.

If you want a permanent configuration, keep it in separate files and let `niri-genconfig` handle the final `config.kdl`.
