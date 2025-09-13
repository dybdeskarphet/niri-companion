## [2.1.0] - 2025-09-13

### 🚀 Features

- *(utils)* Add error logging to Logger utility
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
