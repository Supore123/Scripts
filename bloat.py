#!/usr/bin/env python3
# DESC: Full-featured disk bloat analyzer with color-coded folder bars and improved visualization.
# TAG: filesystem, disk, analysis, bloat, cleanup
# ARG: [DIRECTORY] - Directory to scan (optional, defaults to current working directory)
# ARG: --top N - Number of top files/folders to display (default 20)
# ARG: --min-size SIZE - Minimum file size to include (e.g., 10MB, 500KB)
# ARG: --max-depth N - Maximum folder depth to scan (default unlimited)
# EXAMPLE: jydiskbloat
# EXAMPLE: jydiskbloat /mnt/data --top 50 --min-size 10MB --max-depth 3

import os
import sys
import argparse
import shutil

# ANSI color codes
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"

def human_readable_size(size_bytes):
    """Convert bytes to human-readable format (B, KB, MB, GB, TB)."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = 0
    p = float(size_bytes)
    while p >= 1024 and i < len(size_name) - 1:
        p /= 1024
        i += 1
    return f"{p:.2f} {size_name[i]}"

def parse_size(size_str):
    """Parse a human-readable size string like '10MB' into bytes."""
    size_str = size_str.strip().upper()
    multipliers = {'B':1, 'KB':1024, 'MB':1024**2, 'GB':1024**3, 'TB':1024**4}
    for unit, mult in multipliers.items():
        if size_str.endswith(unit):
            try:
                return int(float(size_str[:-len(unit)]) * mult)
            except ValueError:
                break
    raise argparse.ArgumentTypeError(f"Invalid size format: {size_str}")

def scan_files(directory, min_size=0):
    """Recursively scan files and return list of (path, size) above min_size."""
    files_info = []
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    scanned = 0

    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            scanned += 1
            try:
                size = os.path.getsize(file_path)
                if size >= min_size:
                    files_info.append((file_path, size))
            except OSError:
                continue
            # Optional simple loading indicator
            if total_files > 50:
                print(f"\rScanning files... {scanned}/{total_files}", end='', flush=True)
    if total_files > 50:
        print()  # newline after loading
    return files_info

def scan_folders(directory, min_size=0, max_depth=None):
    """Scan folders recursively and calculate cumulative sizes."""
    folder_sizes = {}
    base_depth = directory.rstrip(os.sep).count(os.sep)
    for root, dirs, files in os.walk(directory):
        depth = root.rstrip(os.sep).count(os.sep) - base_depth
        if max_depth is not None and depth > max_depth:
            dirs[:] = []  # Don't go deeper
            continue
        total_size = 0
        for name in files:
            file_path = os.path.join(root, name)
            try:
                size = os.path.getsize(file_path)
                if size >= min_size:
                    total_size += size
            except OSError:
                continue
        folder_sizes[root] = total_size
    return folder_sizes

def color_bar(size, largest_size, max_length=40):
    """Return a colored ASCII bar proportional to size."""
    bar_len = int(size / largest_size * max_length) if largest_size > 0 else 0
    # Color thresholds: <10% green, 10-50% yellow, >50% red
    ratio = size / largest_size if largest_size > 0 else 0
    if ratio < 0.1:
        color = Colors.GREEN
    elif ratio < 0.5:
        color = Colors.YELLOW
    else:
        color = Colors.RED
    bar = '#' * bar_len
    return f"{color}{bar}{Colors.RESET}"

def print_top_files(files_info, top_n):
    print(f"Top {top_n} largest files:\n")
    files_info.sort(key=lambda x: x[1], reverse=True)
    for file_path, size in files_info[:top_n]:
        print(f"{human_readable_size(size):>10} - {file_path}")

def print_top_folders(folders_info, top_n):
    print(f"\nTop {top_n} largest folders:\n")
    sorted_folders = sorted(folders_info.items(), key=lambda x: x[1], reverse=True)
    largest_size = sorted_folders[0][1] if sorted_folders else 1
    for folder, size in sorted_folders[:top_n]:
        bar = color_bar(size, largest_size)
        print(f"{human_readable_size(size):>10} | {bar} {folder}")

def main():
    parser = argparse.ArgumentParser(description="Disk Bloat Analyzer")
    parser.add_argument('directory', nargs='?', default=os.getcwd(), help="Directory to scan")
    parser.add_argument('--top', type=int, default=20, help="Number of top files/folders to display")
    parser.add_argument('--min-size', type=parse_size, default=0, help="Minimum file size to include (e.g., 10MB)")
    parser.add_argument('--max-depth', type=int, default=None, help="Maximum folder depth to scan")
    args = parser.parse_args()

    print(f"Scanning directory: {os.path.abspath(args.directory)}...\n")

    files_info = scan_files(args.directory, min_size=args.min_size)
    total_size = sum(size for _, size in files_info)
    print(f"Total files scanned: {len(files_info)}")
    print(f"Total size: {human_readable_size(total_size)}\n")

    print_top_files(files_info, args.top)

    folders_info = scan_folders(args.directory, min_size=args.min_size, max_depth=args.max_depth)
    print_top_folders(folders_info, args.top)

if __name__ == "__main__":
    main()

