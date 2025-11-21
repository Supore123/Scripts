#!/usr/bin/env python3
# DESC: Adjust screen brightness (show current in value and %, set absolute or percentage).
#       Auto-elevates: will re-run with sudo or pkexec if not run as root.

import os
import sys
import shutil
import subprocess

BACKLIGHT_PATH = "/sys/class/backlight"

def ensure_root():
    """If not root, try to re-run the script with sudo or pkexec."""
    if os.geteuid() == 0:
        return  # already root

    # Build the command to re-run this python script with the same args
    python = sys.executable or "/usr/bin/env python3"
    args = [python] + sys.argv

    # Try sudo first
    if shutil.which("sudo"):
        try:
            os.execvp("sudo", ["sudo"] + args)
        except OSError:
            pass

    # Fallback to pkexec
    if shutil.which("pkexec"):
        try:
            os.execvp("pkexec", ["pkexec"] + args)
        except OSError:
            pass

    # If nothing works, inform the user
    print("This action requires root. Install or enable 'sudo' or 'pkexec', or run as root.")
    sys.exit(1)

def list_backlight():
    try:
        return os.listdir(BACKLIGHT_PATH)
    except FileNotFoundError:
        return []

def get_max_brightness(backlight):
    with open(os.path.join(BACKLIGHT_PATH, backlight, "max_brightness")) as f:
        return int(f.read().strip())

def get_current_brightness(backlight):
    with open(os.path.join(BACKLIGHT_PATH, backlight, "brightness")) as f:
        return int(f.read().strip())

def set_brightness(backlight, value):
    try:
        value = int(value)
        max_brightness = get_max_brightness(backlight)
        if value < 0 or value > max_brightness:
            print(f"Value must be between 0 and {max_brightness}")
            return
        with open(os.path.join(BACKLIGHT_PATH, backlight, "brightness"), "w") as f:
            f.write(str(value))
        percent = value * 100 // max_brightness
        print(f"Brightness set to {value}/{max_brightness} ({percent}%)")
    except PermissionError:
        print("Permission denied: try running with sudo")
    except Exception as e:
        print(f"Error: {e}")

def show_help():
    print("""Usage: brightness.py [OPTION]

No arguments       Show current brightness (value and %)
<number>           Set brightness to absolute value (0 to max)
<number>%          Set brightness to percentage of max (e.g. 50%)
--help             Show this help message

Examples:
  ./brightness.py         # show current
  ./brightness.py 400     # set absolute value
  ./brightness.py 50%     # set to 50% of max
""")

def main():
    # Auto-elevate if necessary so writing to /sys/class/backlight works
    ensure_root()

    backlights = list_backlight()
    if not backlights:
        print("No backlight interfaces found under /sys/class/backlight")
        return
    backlight = backlights[0]
    max_brightness = get_max_brightness(backlight)

    if len(sys.argv) == 1:
        current = get_current_brightness(backlight)
        percent = current * 100 // max_brightness
        print(f"Current brightness: {current}/{max_brightness} ({percent}%)")
        return

    arg = sys.argv[1]
    if arg in ("--help", "-h"):
        show_help()
        return

    percent = int(arg[0])
    if percent < 0 or percent > 100:
        print("Percentage must be between 0% and 100%")
        return
    value = max_brightness * percent // 100

    set_brightness(backlight, value)

if __name__ == "__main__":
    main()

