# Linux Project Bootstrapper

A file system watcher that automatically organizes and catalogs development projects on Linux systems.

## Overview

The Linux Project Bootstrapper is a Python-based automation tool that monitors your file system in real-time. When it detects the creation of source files in recognized project formats, it automatically moves the project to a centralized location and initializes Docker configuration scaffolding.

## Features

- **Real-time Monitoring**: Watches for file system events across all subdirectories
- **Intelligent Project Detection**: Identifies projects by locating `package.json` files
- **Automatic Organization**: Moves complete projects to a centralized destination directory
- **Docker Integration**: Automatically creates Docker compose configuration files
- **Format Support**: Detects projects with the following file types:
  - JavaScript (`.js`)
  - TypeScript (`.ts`, `.tsx`)
  - Python (`.py`)
  - React JSX (`.jsx`)
  - JSON (`.json`)

## Prerequisites

- Python 3.6 or higher
- `watchdog` library

## Installation

1. Clone or download the repository:
```bash
git clone <repository-url>
cd linux-project-bootstrapper
```

2. Install required dependencies:
```bash
pip install watchdog
```

## Configuration

Edit the following constants in `linux-project-bootstrapper.py` to customize behavior:

```python
DESTINATION = "/home/matias/Desktop/projects"          # Where projects are moved
DOCKER_DESTINATION = "/home/matias/Desktop/docker"    # Where Docker configs go
VALID_EXTENSIONS = (".js", ".tsx", ".py", ".ts", ".jsx", ".json")  # File types to detect
```

## Usage

Start the bootstrapper:

```bash
python linux-project-bootstrapper.py
```

The script will:
1. Begin monitoring the current directory and all subdirectories
2. Watch for creation of files with recognized extensions
3. When detected, locate the project root folder
4. Move the entire project to `DESTINATION`
5. Create a Docker configuration directory and `docker-compose.yml` file
6. Log all actions to the console

Stop the bootstrapper with `Ctrl+C`.

## How It Works

1. **File Detection**: Monitors file system for new files matching `VALID_EXTENSIONS`
2. **Root Discovery**: Traverses parent directories upward searching for `package.json`
3. **Validation**: Confirms the project root contains valid source files
4. **Organization**: Copies project to centralized destination
5. **Initialization**: Creates Docker infrastructure scaffolding

## Example Workflow

```
$ python linux-project-bootstrapper.py
Project moved to: /home/matias/Desktop/projects/my-app
docker-compose.yml created at: /home/matias/Desktop/docker/my-app/docker-compose.yml
```

## Error Handling

The script gracefully handles:
- Non-existent folders
- Permission denied errors
- Duplicate project names
- Invalid file paths
- File system race conditions

All errors are logged to stdout for debugging.

## Limitations

- Projects are identified by the presence of `package.json` only
- Each project name can only be processed once per session (tracked in `PROCESSED_FOLDERS`)
- Requires Linux file system (uses watchdog observer)

## Troubleshooting

**Projects not being moved:**
- Verify the source directory is accessible
- Check that destination directories exist and are writable
- Ensure the project contains valid file types and a `package.json` file

**Permission errors:**
- Run with appropriate permissions: `sudo python linux-project-bootstrapper.py`
- Verify destination directory permissions: `ls -ld /home/matias/Desktop/projects`

**Performance issues:**
- Large directories with many subdirectories may slow detection
- Consider reducing the number of watched directories

## License

MIT License

## Author

Created for automated Linux project organization and Docker initialization.
