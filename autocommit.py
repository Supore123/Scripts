#!/usr/bin/env python3
# DESC: Smart Logical Block Committer with Auto-Gap and Jitter (Directory Support)
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

def get_last_commit_time(path):
    """Fetches the actual timestamp of the most recent commit for the path."""
    try:
        # Use '.' if directory, else the file path
        target = "." if os.path.isdir(path) else path
        timestamp = run_git_command(["log", "-1", "--format=%at", "--", target])
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
    active_ids = set()
    global_lines = [] 
    
    for line in lines:
        start_match = start_pattern.search(line.strip())
        end_match = end_pattern.search(line.strip())
        
        if start_match:
            c_id = int(start_match.group(1))
            msg = start_match.group(2).strip()
            if c_id not in commit_map: 
                commit_map[c_id] = {"msg": msg, "lines": []}
            active_ids.add(c_id)
            continue
            
        if end_match:
            active_ids.discard(int(end_match.group(1)))
            continue
            
        if not active_ids: 
            global_lines.append(line)
        else:
            for c_id in active_ids: 
                commit_map[c_id]["lines"].append(line)
                
    return commit_map, global_lines

def get_files_to_process(target_path):
    """Returns a list of file paths to process, ignoring .git and binaries."""
    if os.path.isfile(target_path):
        return [target_path]
        
    filepaths = []
    for root, dirs, files in os.walk(target_path):
        if '.git' in dirs: dirs.remove('.git') # don't traverse .git
        for file in files:
            if file.endswith('.bak'): continue # Ignore backup files
            filepaths.append(os.path.join(root, file))
    return filepaths

def main():
    parser = argparse.ArgumentParser(description="Smart Logical Committer (Multi-file)")
    parser.add_argument("path", help="File or directory to incrementally commit")
    parser.add_argument("--auto-gap", action="store_true", help="Fill the time between last commit and now")
    parser.add_argument("--delay", type=float, default=10.0, help="Manual delay minutes (if not using auto-gap)")
    parser.add_argument("-y", "--yes", action="store_true", help="Auto-approve all blocks")
    args = parser.parse_args()

    if not os.path.exists(args.path): 
        print(f"{RED}Path does not exist.{RESET}")
        sys.exit(1)

    target_files = get_files_to_process(args.path)
    
    # Global state across all files
    all_blocks = {}       # c_id -> {"msg": "...", "files": {filepath: lines}}
    file_globals = {}     # filepath -> global_lines
    active_files = set()  # files that actually contain markers

    for filepath in target_files:
        try:
            # Safely read as utf-8, ignore files that throw decode errors (likely binaries)
            with open(filepath, "r", encoding="utf-8", errors="strict") as f: 
                lines = f.readlines()
        except UnicodeDecodeError:
            continue 

        prefix = get_marker_prefix(filepath)
        blocks, globals_lines = parse_logical_blocks(lines, prefix)

        if not blocks: continue

        active_files.add(filepath)
        file_globals[filepath] = globals_lines

        # Aggregate blocks by c_id globally
        for c_id, data in blocks.items():
            if c_id not in all_blocks:
                all_blocks[c_id] = {"msg": data["msg"], "files": {}}
            # If multiple files have the same c_id but different messages, the first one encountered is kept
            all_blocks[c_id]["files"][filepath] = data["lines"]

    if not all_blocks:
        print(f"{RED}No markers found in the specified path.{RESET}")
        sys.exit(1)

    sorted_c_ids = sorted(all_blocks.keys())

    # --- TIME CALCULATION ---
    now = datetime.now()
    if args.auto_gap:
        last_time = get_last_commit_time(args.path)
        if last_time:
            total_gap = (now - last_time).total_seconds() / 60
            avg_delay = total_gap / (len(sorted_c_ids) + 1)
            virtual_time = last_time + timedelta(minutes=avg_delay)
            current_delay = avg_delay
            print(f"{CYAN}Detected gap: {total_gap:.1f}m. Avg delay: {avg_delay:.1f}m.{RESET}")
        else:
            print(f"{YELLOW}No previous commit. Using now - 1 hour.{RESET}")
            virtual_time = now - timedelta(hours=1)
            current_delay = 60 / len(sorted_c_ids)
    else:
        virtual_time = now - timedelta(minutes=args.delay * len(sorted_c_ids))
        current_delay = args.delay

    # --- EXECUTION ---
    # Create backups and initialize file content
    current_content = {}
    for filepath in active_files:
        shutil.copy(filepath, filepath + ".bak")
        current_content[filepath] = list(file_globals[filepath])

    try:
        for c_id in sorted_c_ids:
            data = all_blocks[c_id]
            files_to_commit = []

            # Write the new block data into each corresponding file
            for filepath, lines in data["files"].items():
                current_content[filepath].extend(lines)
                with open(filepath, "w", encoding="utf-8") as f: 
                    f.writelines(current_content[filepath])
                files_to_commit.append(filepath)
            
            # Stage the files modified in this specific commit block
            run_git_command(["add"] + files_to_commit)
            
            env = os.environ.copy()
            d_str = virtual_time.strftime("%Y-%m-%dT%H:%M:%S")
            env["GIT_AUTHOR_DATE"] = d_str
            env["GIT_COMMITTER_DATE"] = d_str
            
            run_git_command(["commit", "-m", data["msg"]], env=env)
            print(f"{GREEN}[{d_str}] ✓ ID {c_id}: {data['msg']} ({len(files_to_commit)} files){RESET}")
            
            # Apply 15% Jitter
            jitter = current_delay * 0.15
            virtual_time += timedelta(minutes=max(0.1, current_delay + random.uniform(-jitter, jitter)))
        
        # Optional: Cleanup backups on success
        for filepath in active_files:
            if os.path.exists(filepath + ".bak"):
                os.remove(filepath + ".bak")

        print(f"\n{GREEN}Success! All blocks pushed to history.{RESET}")
        
    except Exception as e:
        # Restore backups on failure
        for filepath in active_files:
            if os.path.exists(filepath + ".bak"):
                shutil.copy(filepath + ".bak", filepath)
        print(f"{RED}Error: {e}{RESET}")

if __name__ == "__main__":
    main()
