---
title: NIRI-GENCONFIG
section: 1
date: June 2026
header: niri-companion Manual
footer: niri-genconfig 5.0.0
---

# NAME

niri-genconfig - niri-companion config generation tool

# SYNOPSIS

**niri-genconfig** [*OPTIONS*] _COMMAND_ [*ARGS*]...

# DESCRIPTION

**niri-genconfig** manages niri configuration by combining multiple KDL files. It supports grouping sources, allowing users to switch between different visual styles or monitor setups easily.

# OPTIONS

**-h, --help**
: Show help message and exit.

# COMMANDS

## generate [*GROUP*]

Combine source files into the final niri configuration.

**-u, --use-include**
: Instead of merging file contents, write a file containing KDL `include` statements for each source.

**-c, --combine**
: Instead of using `include` statements, merge the contents of each source to the `config.kdl`.

**GROUP**
: Select a specific configuration group. Standalone source strings are always included. Objects matching the group name are included. Defaults to "default".

## daemon [*GROUP*]

Start a daemon that monitors the `watch_dir`. It regenerates the configuration automatically whenever a source file is modified.

**GROUP**
: The configuration group to use for automatic generation.

# CONFIGURATION

Stored in `~/.config/niri-companion/settings.toml`.

## [general]

**output_path**
: Target niri config (e.g., `"~/.config/niri/config.kdl"`).

## [genconfig]

**watch_dir**
: Directory to monitor (default: `"~/.config/niri/sources"`).

**sources**
: List of strings (paths) or arrays of objects (groups).

### Example Configuration

```toml
[genconfig]
sources = [
  "~/niri/base.kdl",
  [
    { group = "default", path = "~/niri/visual_standard.kdl" },
    { group = "cool", path = "~/niri/visual_custom.kdl" },
  ]
]
```

# EXAMPLES

Generate the default configuration:

> **niri-genconfig generate**

Generate a specific group using includes:

> **niri-genconfig generate -u cool**

# SEE ALSO

**niri-ipcext**(1), **niri-workspaces**(1)
