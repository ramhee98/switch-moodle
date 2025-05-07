import os
import subprocess
import shutil
import sys

# Exit script if root permissions are missing 
if os.geteuid() != 0:
    print(f"This script must be run as root. Use 'sudo python3 {__file__}'")
    sys.exit(1)

# Define paths
base_path = "/var/www/"
moodle = os.path.join(base_path, "moodle")
moodle_old = os.path.join(base_path, "moodle_old")
moodle_new = os.path.join(base_path, "moodle_new")

def run_command(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {' '.join(cmd)}\n{e}")
        exit(1)

# Stop Apache
run_command(["systemctl", "stop", "apache2"])

try:
    if os.path.exists(moodle_old):
        print(f"{moodle_old} found. Moving moodle to {moodle_new} and replacing it with {moodle_old}.")
        shutil.move(moodle, moodle_new)
        shutil.move(moodle_old, moodle)
    elif os.path.exists(moodle_new):
        print(f"{moodle_new} found. Moving moodle to {moodle_old} and replacing it with {moodle_new}.")
        shutil.move(moodle, moodle_old)
        shutil.move(moodle_new, moodle)
    else:
        print(f"Neither {moodle_old} nor {moodle_new} exists. Nothing to do.")
except Exception as e:
    print(f"Error while moving directories: {e}")
    exit(1)

# Start Apache
run_command(["systemctl", "start", "apache2"])

print("Operation completed.")
