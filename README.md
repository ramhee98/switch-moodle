# switch-moodle

A simple Python script to switch between Moodle environments on a Debian-based web server.  
This utility stops the webserver, swaps Moodle directories, and restarts the webserver which is useful for quickly testing changes or rolling back to a previous version.

---

## Directory Structure

The script works within the configured `base_path` and manages the following folders:

- `moodle` – current active Moodle installation
- `moodle_old` – a previous version
- `moodle_new` – a temporary or alternate version

These folder names and the base path are configurable via `config.ini`.

---

## How It Works

Depending on which alternate directory exists, the script does the following:

### Case 1: `moodle_old` exists
- Moves `moodle` → `moodle_new`
- Moves `moodle_old` → `moodle`

### Case 2: `moodle_new` exists
- Moves `moodle` → `moodle_old`
- Moves `moodle_new` → `moodle`

If neither exists, nothing is done.

---

## Requirements

- Debian
- python3
- apache2 or nginx
- Root privileges (`sudo`) - the script checks and exits if not run as root
- The script must be executed on the system hosting the Moodle files

---

## Configuration

Before the script runs, it expects a `config.ini` file in the project root directory. This file defines the base path and directory names used for switching Moodle installations.

If `config.ini` does not exist, it will be automatically created from `config_template.ini`.

### `config_template.ini` structure

```ini
[settings]

# Base directory where all Moodle instances are located
base_path = /var/www/

# Name of the Moodle directory loaded by the webserver
moodle = moodle

# Name of the old Moodle directory (e.g. for backup or archive)
moodle_old = moodle_old

# Name of the new Moodle directory (e.g. for upgrade or migration)
moodle_new = moodle_new
```

---

## Usage

```bash
git clone https://github.com/yourusername/switch-moodle.git
cd switch-moodle
sudo python3 switch_moodle.py
```
The script will generate a config.ini file if missing. Edit it as needed.

---

## Contribution

Contributions are welcome! Please fork the repository, create a new branch for your changes, and submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Disclaimer

Use this tool at your own risk. Ensure you have proper backups and permissions before running the script in a production environment.

---

## Author

Developed by [ramhee98](https://github.com/ramhee98). For questions or suggestions, feel free to open an issue in the repository.


