---
title: NIRI-IPCEXT
section: 1
date: May 2026
header: niri-companion Manual
footer: niri-ipcext 4.0.1
---

# NAME
niri-ipcext - niri-companion IPC-like configuration tool

# SYNOPSIS
**niri-ipcext** [*OPTIONS*] *COMMAND* [*ARGS*]...

# DESCRIPTION
**niri-ipcext** simulates IPC behavior by directly modifying the niri configuration file. It is useful for making temporary visual changes (like borders or gaps) without manually editing files.

# OPTIONS
**-h, --help**
:   Show help message and exit.

# COMMANDS

## replace *OLD* *NEW*
Surgically replaces a string in the config file.

**OLD**
:   The exact text to find. Must match spaces and indentation perfectly.

**NEW**
:   The replacement text.

## restore
Wipes manual changes and restores the config to its base state by running **niri-genconfig generate**.

# EXAMPLES
Changing border width from 2 to 10:
> **niri-ipcext replace 'width 2' 'width 10'**

Resetting all temporary changes:
> **niri-ipcext restore**

# NOTES
This tool modifies the file defined in `general.output_path`. Because niri reloads its config when the file is touched, changes take effect immediately.

# SEE ALSO
**niri-genconfig**(1), **niri-workspaces**(1)
