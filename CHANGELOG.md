## [unreleased]

### 🚀 Features

- *(genconfig)* Add --use-include flag and functionality
- *(genconfig)* Remove the --use-include flag from daemon
- *(genconfig)* Watch directories recursively with daemon mode

### 🚜 Refactor

- *(genconfig)* Simplify the config generation function

### ⚙️ Miscellaneous Tasks

- *(release)* Add release body and filter the release files
- *(release)* Bump version
## [3.0.0] - 2025-11-18

### 🚀 Features

- *(genconfig)* [**breaking**] Generate the config when the daemon is started initially

### ⚙️ Miscellaneous Tasks

- *(release)* Create an automatic release action
- *(release)* Bump version
## [2.4.0] - 2025-10-26

### 🚀 Features

- *(nix)* Add default and shell Nix configurations for niri-companion
- *(config)* Add per item task_delay option to workspaces
- *(config)* Add defaults for some of the config options
- *(workspaces)* Use the per item task_delay option if available

### 🐛 Bug Fixes

- *(nix)* Update test configuration to run pytest and limit imports during checks
- *(workspaces)* Shorten the additional delays

### ⚙️ Miscellaneous Tasks

- *(release)* Bump version
- *(nix)* Bump version for default.nix
## [2.3.0] - 2025-09-24

### 🚀 Features

- *(genconfig)* Add config groups feature
- *(genconfig)* Add group selection option to genconfig daemon mode

### 🐛 Bug Fixes

- *(ipcext)* Write a description suitable for ipcext
- *(pyproject)* Use the appropriate method to call scripts that use Typer

### 💼 Other

- *(deps)* Add Typer

### 🚜 Refactor

- Overall modularization of the project and better CLI arg handling/logging
- *(config)* Split load_config to multiple methods

### 🧪 Testing

- *(utils)* Add tests for utils

### ⚙️ Miscellaneous Tasks

- *(ci)* Add gitcliff action
- *(ci)* Rename .workflows to workflows
- *(ci)* Add missing sections to git-cliff action
- *(utils)* Rename creat_dir with create_dir
- *(wiki)* Add github-wiki-action
- *(cliff)* Ignore docs tag for CHANGELOG generation
- *(ipcext)* Remove unnecessary import
- *(release)* Bump version
## [2.2.0] - 2025-09-20

### 🚀 Features

- *(utils)* Use colorful logging for home not found error
- *(utils)* Add warn to logger
- *(utils)* Create expandall for quickly expanding env variables and tilde
- *(config)* Prompt for an default niri-companion config if no config is found
- *(config)* Change invalid config error table style

### 💼 Other

- *(deps)* Add tomli-w
- *(release)* Bump version to 2.2.0

### 🚜 Refactor

- *(config)* Use the expandall util

### ⚙️ Miscellaneous Tasks

- *(precommit)* Add conventional commit messages pre-commit hook
## [2.1.0] - 2025-09-13

### 🚀 Features

- *(utils)* Add error loggin to Logger utility
- *(utils)* Copy config path generation logic to ConfigPath for future use
- *(config)* Pretty print errors and use ConfigPath utility

### 🐛 Bug Fixes

- Use the utils path instead of logger path for other modules

### 💼 Other

- *(deps)* Add rich to dependencies

### ⚙️ Miscellaneous Tasks

- *(examples)* Update settings.toml
- Rename logger as utils
- Bump version
## [2.0.0] - 2025-09-11

### 🚀 Features

- *(genconfig)* Exit if genconfig.sources has non-existent file(s)
- *(genconfig)* Add daemon mode to genconfig
- *(logger)* Add logger for verbose and colorful outputs
- Give colorful outputs using logger and ANSI escape sequences

### 💼 Other

- *(deps)* Add watchdog for genconfig daemon mode

### 🚜 Refactor

- *(config)* Use list[str] instead of list[Path] with sources

### ⚙️ Miscellaneous Tasks

- Update uv.lock
- Bump version
## [1.0.0] - 2025-09-10

### ⚙️ Miscellaneous Tasks

- *(git-cliff)* Add CHANGELOG and cliff.toml
- *(release)* V1.0.0
## [0.1.0] - 2025-09-10
