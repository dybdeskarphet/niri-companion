---
title: NIRI-WORKSPACES
section: 1
date: May 2026
header: niri-companion Manual
footer: niri-workspaces 5.0.0
---

# NAME

niri-workspaces - niri-companion workspace management tool

# SYNOPSIS

**niri-workspaces**

# DESCRIPTION

**niri-workspaces** manages complex workspace layouts. It presents a list of workspaces via a dmenu-compatible picker (like rofi). Selecting a workspace triggers a sequence of commands to open specific applications on specific workspaces.

# CONFIGURATION

Stored in `~/.config/niri-companion/settings.toml`.

## [workspaces]

**dmenu_command**
: Picker command (default: `"rofi -dmenu"`).

**task_delay**
: Default wait time in seconds between starting applications.

## [workspaces.items]

Defines the workspaces available in the picker. Each item is a list of task objects.

### Task Object Fields

**workspace**
: Target workspace number.

**run**
: Shell command to execute.

**task_delay**
: (Optional) Specific delay for this task.

# EXAMPLES

## Example Workspace Setup

```toml
[workspaces.items]
"dev" = [
  { workspace = 1, run = 'foot -e nvim' },
  { workspace = 2, run = 'brave --new-window github.com', task_delay = 1.5 }
]
```

## Usage

Running the tool:

> **niri-workspaces**

Selecting "dev" will:

1. Open a terminal with nvim on workspace 1.
2. Wait 0.8s (default).
3. Open Brave on workspace 2.
4. Wait 1.5s (specific override).

# SEE ALSO

**niri-genconfig**(1), **niri-ipcext**(1)
