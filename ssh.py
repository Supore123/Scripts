#!/usr/bin/env python3
# DESC: Quick SSH connection manager with host shortcuts
# ARG: --list          List all saved hosts
# ARG: --add           Add a new host
# ARG: --remove        Remove a host
# ARG: --host NAME     Connect to a specific host by name
# ARG: --user USER     SSH username (overrides saved)
# ARG: --port PORT     SSH port (overrides saved)
# ARG: --identity FILE SSH identity file (optional)

import os, json, argparse, subprocess, sys

CONFIG_PATH = os.path.expanduser("~/.jyssh.json")

# Load or initialize config
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        json.dump({}, f, indent=4)

with open(CONFIG_PATH) as f:
    hosts = json.load(f)

# -------------------------
# CLI Arguments
# -------------------------
parser = argparse.ArgumentParser(description="SSH shortcut manager")
parser.add_argument("--list", action="store_true", help="List saved hosts")
parser.add_argument("--add", action="store_true", help="Add a new host")
parser.add_argument("--remove", action="store_true", help="Remove a host")
parser.add_argument("--host", type=str, help="Host shortcut name to connect")
parser.add_argument("--user", type=str, help="SSH username override")
parser.add_argument("--port", type=int, help="SSH port override")
parser.add_argument("--identity", type=str, help="SSH identity file")
args = parser.parse_args()

# -------------------------
# Helper Functions
# -------------------------
def save_config():
    with open(CONFIG_PATH, "w") as f:
        json.dump(hosts, f, indent=4)

def list_hosts():
    if not hosts:
        print("[*] No hosts saved yet.")
        return
    print("\nSaved hosts:")
    for name, info in hosts.items():
        print(f"- {name}: {info['user']}@{info['hostname']}:{info.get('port',22)}")
    print()

def add_host():
    name = input("Shortcut name: ").strip()
    hostname = input("Hostname/IP: ").strip()
    user = input("Username: ").strip()
    port = input("Port [22]: ").strip()
    port = int(port) if port else 22
    hosts[name] = {"hostname": hostname, "user": user, "port": port}
    save_config()
    print(f"[*] Host '{name}' added!")

def remove_host():
    list_hosts()
    name = input("Shortcut name to remove: ").strip()
    if name in hosts:
        del hosts[name]
        save_config()
        print(f"[*] Host '{name}' removed!")
    else:
        print(f"[ERROR] Host '{name}' not found.")

def connect_host(name):
    if name not in hosts:
        print(f"[ERROR] Host '{name}' not found in saved hosts.")
        sys.exit(1)
    info = hosts[name]
    user = args.user or info["user"]
    hostname = info["hostname"]
    port = args.port or info.get("port", 22)
    identity = args.identity
    cmd = ["ssh"]
    if identity: cmd += ["-i", identity]
    cmd += ["-p", str(port), f"{user}@{hostname}"]
    print(f"[*] Connecting to {user}@{hostname}:{port} ...")
    subprocess.run(cmd)

# -------------------------
# Main Logic
# -------------------------
if args.list:
    list_hosts()
    sys.exit(0)

if args.add:
    add_host()
    sys.exit(0)

if args.remove:
    remove_host()
    sys.exit(0)

if args.host:
    connect_host(args.host)
else:
    # Interactive menu if no host provided
    if not hosts:
        print("[*] No hosts saved. Use --add to add a host.")
        sys.exit(0)
    print("\nAvailable hosts:")
    for i, name in enumerate(hosts.keys(), start=1):
        info = hosts[name]
        print(f"{i}. {name}: {info['user']}@{info['hostname']}:{info.get('port',22)}")
    choice = input(f"Select host [1-{len(hosts)}]: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(hosts)):
        print("[ERROR] Invalid choice")
        sys.exit(1)
    selected = list(hosts.keys())[int(choice)-1]
    connect_host(selected)
