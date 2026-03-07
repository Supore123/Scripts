#!/usr/bin/env python3
# DESC: Smart Logical Block Committer with Auto-Gap and Jitter
# SCHEMA: # START_COMMIT(id): message ... # END_COMMIT(id)

import os
import sys
import shutil
import subprocess
import argparse
import time
import random
import re
from datetime import datetime, timedelta

# Colors
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
RESET = "\033[0m"

def run_git_command(args, env=None):
    try:
        result = subprocess.run(["git"] + args, check=True, capture_output=True, text=True, env=env)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"{RED}Git error: {e.stderr.strip()}{RESET}")
        sys.exit(1)

def get_last_commit_time(filename):
    """Fetches the actual timestamp of the most recent commit for the file."""
    try:
        timestamp = run_git_command(["log", "-1", "--format=%at", "--", filename])
        if not timestamp: return None
        return datetime.fromtimestamp(int(timestamp))
    except:
        return None

def get_marker_prefix(filename):
    ext = os.path.splitext(filename)[1].lower()
    c_style_exts = {'.c', '.cpp', '.cxx', '.h', '.hpp', '.java', '.js', '.ts', '.cs', '.go', '.rs', '.swift'}
    return "//" if ext in c_style_exts else "#"

def parse_logical_blocks(lines, prefix):
    commit_map = {}
    start_pattern = re.compile(rf"^{re.escape(prefix)}\s*START_COMMIT\((\d+)\):\s*(.*)", re.IGNORECASE)
    end_pattern = re.compile(rf"^{re.escape(prefix)}\s*END_COMMIT\((\d+)\)", re.IGNORECASE)
    active_ids = set(); global_lines = [] 
    for line in lines:
        start_match = start_pattern.search(line.strip())
        end_match = end_pattern.search(line.strip())
        if start_match:
            c_id = int(start_match.group(1))
            msg = start_match.group(2).strip()
            if c_id not in commit_map: commit_map[c_id] = {"msg": msg, "lines": []}
            active_ids.add(c_id); continue
        if end_match:
            active_ids.discard(int(end_match.group(1))); continue
        if not active_ids: global_lines.append(line)
        else:
            for c_id in active_ids: commit_map[c_id]["lines"].append(line)
    return dict(sorted(commit_map.items())), global_lines

def main():
    parser = argparse.ArgumentParser(description="Smart Logical Committer")
    parser.add_argument("file", help="The file to incrementally commit")
    parser.add_argument("--auto-gap", action="store_true", help="Fill the time between last commit and now")
    parser.add_argument("--delay", type=float, default=10.0, help="Manual delay minutes (if not using auto-gap)")
    parser.add_argument("-y", "--yes", action="store_true", help="Auto-approve all blocks")
    args = parser.parse_args()

    if not os.path.exists(args.file): sys.exit(1)
    with open(args.file, "r") as f: lines = f.readlines()
    prefix = get_marker_prefix(args.file)
    blocks, globals = parse_logical_blocks(lines, prefix)

    if not blocks:
        print(f"{RED}No markers found.{RESET}"); sys.exit(1)

    # --- TIME CALCULATION ---
    now = datetime.now()
    if args.auto_gap:
        last_time = get_last_commit_time(args.file)
        if last_time:
            total_gap = (now - last_time).total_seconds() / 60
            avg_delay = total_gap / (len(blocks) + 1)
            virtual_time = last_time + timedelta(minutes=avg_delay)
            current_delay = avg_delay
            print(f"{CYAN}Detected gap: {total_gap:.1f}m. Avg delay: {avg_delay:.1f}m.{RESET}")
        else:
            print(f"{YELLOW}No previous commit. Using now - 1 hour.{RESET}")
            virtual_time = now - timedelta(hours=1)
            current_delay = 60 / len(blocks)
    else:
        virtual_time = now - timedelta(minutes=args.delay * len(blocks))
        current_delay = args.delay

    # --- EXECUTION ---
    backup_path = args.file + ".bak"
    shutil.copy(args.file, backup_path)
    current_content = list(globals)

    try:
        for c_id, data in blocks.items():
            current_content.extend(data["lines"])
            with open(args.file, "w") as f: f.writelines(current_content)
            
            run_git_command(["add", args.file])
            env = os.environ.copy()
            d_str = virtual_time.strftime("%Y-%m-%dT%H:%M:%S")
            env["GIT_AUTHOR_DATE"] = d_str
            env["GIT_COMMITTER_DATE"] = d_str
            
            run_git_command(["commit", "-m", data["msg"]], env=env)
            print(f"{GREEN}[{d_str}] ✓ {data['msg']}{RESET}")
            
            # Apply 15% Jitter
            jitter = current_delay * 0.15
            virtual_time += timedelta(minutes=max(0.1, current_delay + random.uniform(-jitter, jitter)))
        
        print(f"\n{GREEN}Success! All blocks pushed to history.{RESET}")
    except Exception as e:
        shutil.copy(backup_path, args.file)
        print(f"{RED}Error: {e}{RESET}")

if __name__ == "__main__":
    main()
