# switch-moodle

A simple Python script to switch between Moodle environments on a Debian-based web server.  
This utility stops Apache, swaps Moodle directories, and restarts Apache wich is useful for quickly testing changes or rolling back to a previous version.

---

## Directory Structure

The script works within `/var/www/` and manages the following folders:

- `moodle` – current active Moodle installation
- `moodle_old` – a previous version
- `moodle_new` – a temporary or alternate version

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
- apache2
- Root privileges (`sudo`)
- The script must be executed on the system hosting the Moodle files

---

## Usage

```bash
git clone https://github.com/yourusername/switch-moodle.git
cd switch-moodle
sudo python3 switch_moodle.py
```

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


