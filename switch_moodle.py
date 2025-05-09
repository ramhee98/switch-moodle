import os
import subprocess
import shutil
import sys
import configparser
import apt

# Exit script if root permissions are missing 
if os.geteuid() != 0:
    print(f"This script must be run as root. Use 'sudo python3 {__file__}'")
    sys.exit(1)

cache = apt.Cache()  # Load package cache once and reuse

def restart_webserver(action):
        """start / stop the apache or nginx webserver, depending on which one is installed"""
        webserver = None

        if cache["apache2"].is_installed:
            webserver = "apache2"
        elif cache["nginx"].is_installed:
            webserver = "nginx"

        if not webserver:
            print("No supported web server found (Apache/Nginx)")
            return

        print(f"Attempting to {action} the {webserver} service")
        run_command(["systemctl", action, webserver])

# Define config files with base path relative to script location
script_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(script_dir, "config.ini")
template_file = os.path.join(script_dir, "config_template.ini")

# Determine the original user (not root)
original_uid = int(os.environ.get("SUDO_UID", os.getuid()))
original_gid = int(os.environ.get("SUDO_GID", os.getgid()))

# Create config.ini from template if missing
if not os.path.exists(config_file):
    if os.path.exists(template_file):
        shutil.copy(template_file, config_file)
        os.chown(config_file, original_uid, original_gid)
        print(f"{config_file} not found. Created from {template_file} and ownership set to original user.")
    else:
        print("Missing both config.ini and config_template.ini. Cannot proceed.")
        sys.exit(1)

# Parse config.ini
config = configparser.ConfigParser()
config.read(config_file)

try:
    # Define paths
    base_path = config["settings"]["base_path"]
    moodle = os.path.join(base_path, config["settings"]["moodle"])
    moodle_old = os.path.join(base_path, config["settings"]["moodle_old"])
    moodle_new = os.path.join(base_path, config["settings"]["moodle_new"])
except KeyError as e:
    print(f"Missing config value: {e}")
    sys.exit(1)

def run_command(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {' '.join(cmd)}\n{e}")
        exit(1)

try:
    if os.path.exists(moodle_old):
        moodle_to_deactivate = moodle_new
        moodle_to_activate = moodle_old
    elif os.path.exists(moodle_new):
        moodle_to_deactivate = moodle_old
        moodle_to_activate = moodle_new
    else:
        print(f"Neither {moodle_old} nor {moodle_new} exists. Nothing to do")
    if os.path.exists(moodle_old) or os.path.exists(moodle_new):
        restart_webserver("stop")
        print(f"{moodle_to_activate} found. Moving {moodle} to {moodle_to_deactivate} and replacing it with {moodle_to_activate}")
        shutil.move(moodle, moodle_to_deactivate)
        shutil.move(moodle_to_activate, moodle)
        restart_webserver("start")
        print(f"Operation completed. {moodle_to_activate} activated")
except Exception as e:
    print(f"Error while moving directories: {e}")
    exit(1)
