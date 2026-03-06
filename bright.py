#!/usr/bin/env python3
# DESC: Adjust screen brightness (show current in value and %, set absolute or percentage).
#       Smart auto-elevates: only requests sudo if the brightness file isn't already writable.

import os
import sys
import shutil

BACKLIGHT_PATH = "/sys/class/backlight"

def ensure_write_access(brightness_file):
    """Check if we can write to the file; if not, elevate privileges."""
    # If we already have write access (e.g., via udev rule), do nothing
    if os.access(brightness_file, os.W_OK):
        return

    # If not writable, and we aren't root, elevate
    if os.geteuid() != 0:
        python = sys.executable or "/usr/bin/env python3"
        args = [python] + sys.argv

        if shutil.which("sudo"):
            try:
                os.execvp("sudo", ["sudo"] + args)
            except OSError:
                pass

        if shutil.which("pkexec"):
            try:
                os.execvp("pkexec", ["pkexec"] + args)
            except OSError:
                pass

        print("Error: Cannot write to brightness file. Set up udev rules or run as root.")
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
    max_brightness = get_max_brightness(backlight)
    if value < 0 or value > max_brightness:
        print(f"Value must be between 0 and {max_brightness}")
        return
        
    brightness_file = os.path.join(BACKLIGHT_PATH, backlight, "brightness")
    
    # Ensure we have permissions before attempting to write
    ensure_write_access(brightness_file)
    
    try:
        with open(brightness_file, "w") as f:
            f.write(str(value))
        percent = value * 100 // max_brightness
        print(f"Brightness set to {value}/{max_brightness} ({percent}%)")
    except Exception as e:
        print(f"Error writing to file: {e}")

def show_help():
    print("""Usage: brightness.py [OPTION]

No arguments       Show current brightness (value and %)
<number>           Set brightness to absolute value (0 to max)
<number>%          Set brightness to percentage of max (e.g. 50%)
--help, -h         Show this help message

Examples:
  ./brightness.py         # show current
  ./brightness.py 400     # set absolute value
  ./brightness.py 50%     # set to 50% of max
""")

def main():
    backlights = list_backlight()
    if not backlights:
        print("No backlight interfaces found under /sys/class/backlight")
        return
    
    # Defaults to the first backlight found
    backlight = backlights[0]
    max_brightness = get_max_brightness(backlight)

    # No arguments: Show current
    if len(sys.argv) == 1:
        current = get_current_brightness(backlight)
        percent = current * 100 // max_brightness
        print(f"Current brightness: {current}/{max_brightness} ({percent}%)")
        return

    arg = sys.argv[1]
    
    # Help menu
    if arg in ("--help", "-h"):
        show_help()
        return

    # Parse percentage vs absolute
    try:
        if arg.endswith("%"):
            percent = int(arg[:-1]) # Strip the '%' and convert to int
            if percent < 0 or percent > 100:
                print("Percentage must be between 0% and 100%")
                return
            value = max_brightness * percent // 100
        else:
            value = int(arg)
    except ValueError:
        print(f"Invalid argument: '{arg}'. Must be a number or percentage.")
        return

    set_brightness(backlight, value)

if __name__ == "__main__":
    main()
