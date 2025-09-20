## [unreleased]

### ⚙️ Miscellaneous Tasks

- *(ci)* Add gitcliff action
- *(ci)* Rename .workflows to workflows
- *(ci)* Add missing sections to git-cliff action
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

### 📚 Documentation

- *(CHANGELOG)* V2.1.0
- *(README)* Add LICENSE badge
- *(README)* Add pypi link to badges
- *(README)* Use total downloads instead of daily downloads

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

### 📚 Documentation

- *(CHANGELOG)* Update CHANGELOG
- *(README)* Add more information about the usage
- Add LICENSE and update pyproject.toml
- *(README)* Add shields and stuff
- *(README)* Add CHANGELOG notice

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

### 📚 Documentation

- Update CHANGELOG
- *(README)* Correct the grammatical errors
- *(README)* Delete the extra new line
- *(README)* Improve grammar

### ⚙️ Miscellaneous Tasks

- Update uv.lock
- Bump version
## [1.0.0] - 2025-09-10

### ⚙️ Miscellaneous Tasks

- *(git-cliff)* Add CHANGELOG and cliff.toml
- *(release)* V1.0.0
## [0.1.0] - 2025-09-10
