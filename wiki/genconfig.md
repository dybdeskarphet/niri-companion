# Configuration

The configuration file is located at:

```
~/.config/niri-companion/settings.toml
```

> [!NOTE]
> All TOML snippets below are **examples**. Your setup may differ depending on your paths, file structure, or preferred groups.

## General Settings

Set up your output file path first. This is usually something like:

```toml
[general]
output_path = "~/.config/niri/config.kdl"
```

## `genconfig` Options

These settings control how your Niri configuration is generated. A sample setup might look like:

```toml
[genconfig]
watch_dir = "$XDG_CONFIG_HOME/niri/src"
sources = [
  "$XDG_CONFIG_HOME/niri/src/internal.kdl",
  "$XDG_CONFIG_HOME/niri/src/monitors.kdl",
  [
    { group = "default", path = "$XDG_CONFIG_HOME/niri/src/visual.kdl" },
    { group = "cool", path = "$XDG_CONFIG_HOME/niri/src/visual_custom.kdl" },
  ],
  "$XDG_CONFIG_HOME/niri/src/input.kdl",
  "$XDG_CONFIG_HOME/niri/src/keybindings.kdl",
  "$XDG_CONFIG_HOME/niri/src/rules.kdl",
]
```

> [!NOTE]
> This is just one way to structure your sources. You can add or remove files, or define different groups as you like.

### `watch_dir`

This directory is monitored when you run:

```
niri-genconfig daemon
```

If files inside this directory change, the daemon automatically regenerates your `output_path` configuration file.

### `sources`

Define all the KDL configuration files you want to combine. You can split your configs across multiple files and groups.

#### Grouping

You can define *config groups* inside `sources` using an array of objects. For example:

```toml
sources = [
  "$XDG_CONFIG_HOME/niri/src/internal.kdl",
  "$XDG_CONFIG_HOME/niri/src/monitors.kdl",
  [
    { group = "default", path = "$XDG_CONFIG_HOME/niri/src/visual.kdl" },
    { group = "cool", path = "$XDG_CONFIG_HOME/niri/src/visual_cool.kdl" },
  ],
  "$XDG_CONFIG_HOME/niri/src/input.kdl",
  "$XDG_CONFIG_HOME/niri/src/keybindings.kdl",
  "$XDG_CONFIG_HOME/niri/src/rules.kdl",
]
```

Only the files from the selected group (plus any standalone string items) are included when generating the config. For example:

```
niri-genconfig generate cool
```

Would combine:

```
$XDG_CONFIG_HOME/niri/src/internal.kdl
$XDG_CONFIG_HOME/niri/src/monitors.kdl
$XDG_CONFIG_HOME/niri/src/visual_cool.kdl
$XDG_CONFIG_HOME/niri/src/input.kdl
$XDG_CONFIG_HOME/niri/src/keybindings.kdl
$XDG_CONFIG_HOME/niri/src/rules.kdl
```

If no group is specified, the `default` group is used automatically.

# Usage

### Generate Configuration

```
niri-genconfig generate
```

Generates your `config.kdl` (or your custom `output_path`) using your `genconfig` settings.

You can specify a group:

```
niri-genconfig generate cool
```

### Run as Daemon

```
niri-genconfig daemon
```

Watches your `genconfig.watch_dir` for changes and regenerates your config automatically.

Groups work with the daemon too:

```
niri-genconfig daemon cool
```
