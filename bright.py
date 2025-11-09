#!/usr/bin/env python3
# DESC: Adjust screen brightness (show current, set absolute value, or set percentage)

import os
import sys

def list_backlight():
    path = "/sys/class/backlight"
    return os.listdir(path)

def get_max_brightness(backlight):
    with open(f"/sys/class/backlight/{backlight}/max_brightness") as f:
        return int(f.read().strip())

def get_current_brightness(backlight):
    with open(f"/sys/class/backlight/{backlight}/brightness") as f:
        return int(f.read().strip())

def set_brightness(backlight, value):
    try:
        value = int(value)
        max_brightness = get_max_brightness(backlight)
        if value < 0 or value > max_brightness:
            print(f"Value must be between 0 and {max_brightness}")
            return
        with open(f"/sys/class/backlight/{backlight}/brightness", "w") as f:
            f.write(str(value))
        print(f"Brightness set to {value}/{max_brightness}")
    except PermissionError:
        print("Permission denied: try running with sudo")
    except Exception as e:
        print(f"Error: {e}")

def show_help():
    print("""
Usage: brightness.py [OPTION]

No arguments       Show current brightness
<number>           Set brightness to absolute value (0 to max)
<number>%          Set brightness to percentage of max
--help             Show this help message
""")

def main():
    backlights = list_backlight()
    if not backlights:
        print("No backlight interfaces found")
        return
    backlight = backlights[0]
    max_brightness = get_max_brightness(backlight)

    if len(sys.argv) == 1:
        current = get_current_brightness(backlight)
        print(f"Current brightness: {current}/{max_brightness}")
        return

    arg = sys.argv[1]
    if arg == "--help":
        show_help()
        return

    # Handle percentages
    if arg.endswith("%"):
        try:
            percent = int(arg[:-1])
            value = max_brightness * percent // 100
        except ValueError:
            print("Invalid percentage format")
            return
    else:
        try:
            value = int(arg)
        except ValueError:
            print("Invalid brightness value")
            return

    set_brightness(backlight, value)

if __name__ == "__main__":
    main()

