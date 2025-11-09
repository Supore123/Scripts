#!/usr/bin/env python3
# DESC: Quick SSH connection manager with host shortcuts
# ARG: --list          List all saved hosts
# ARG: --add           Add a new host
# ARG: --remove        Remove a host
# ARG: --host NAME     Connect to a specific host by name
# ARG: --user USER     SSH username (overrides saved)
# ARG: --port PORT     SSH port (overrides saved)
# ARG: --identity FILE SSH identity file (optional)
# ARG: --setup-key NAME Generate/local key and copy public key to host (password required once)
# ARG: --no-ask         Non-interactive prompts (use with care when scripting)

import os
import json
import argparse
import subprocess
import sys
import shutil
import getpass

CONFIG_PATH = os.path.expanduser("~/.jyssh.json")
DEFAULT_KEY_PATH = os.path.expanduser("~/.ssh/id_ed25519")
SSH_COPY_ID = shutil.which("ssh-copy-id")
SSHPASS = shutil.which("sshpass")

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
parser.add_argument("--setup-key", type=str, help="Generate/local key (if missing) and copy public key to named host")
parser.add_argument("--no-ask", action="store_true", help="Non-interactive mode for scripting (use with care)")
args = parser.parse_args()

# -------------------------
# Helper Functions
# -------------------------
def save_config():
    with open(CONFIG_PATH, "w") as f:
        json.dump(hosts, f, indent=4)
    print("[*] Config saved.")

def list_hosts():
    if not hosts:
        print("[*] No hosts saved yet.")
        return
    print("\nSaved hosts:")
    for name, info in hosts.items():
        display_port = info.get("port", 22)
        display_identity = info.get("identity", "")
        pw_set = "yes" if info.get("password") else "no"
        print(f"- {name}: {info['user']}@{info['hostname']}:{display_port}  identity={display_identity or 'none'}  password_stored={pw_set}")
    print()

def prompt(prompt_text, default=None, allow_empty=False):
    if args.no_ask:
        return default
    val = input(f"{prompt_text}" + (f" [{default}]" if default is not None else "") + ": ").strip()
    if val == "" and not allow_empty:
        return default
    return val

def add_host():
    name = prompt("Shortcut name").strip()
    if not name:
        print("[ERROR] Name required.")
        return
    hostname = prompt("Hostname/IP").strip()
    user = prompt("Username").strip()
    port = prompt("Port", "22").strip()
    port = int(port) if port else 22

    identity = prompt("Identity file (leave blank to use default key)", "").strip()
    if identity == "":
        identity = None

    store_pw = prompt("Store password for this host? (insecure) (y/N)", "N").lower()
    password = None
    if store_pw == "y":
        if args.no_ask:
            print("[ERROR] --no-ask prevents interactive password entry.")
            return
        password = getpass.getpass("Password to store (will be saved in plain text; insecure): ").strip()
        confirm = getpass.getpass("Confirm password: ").strip()
        if password != confirm:
            print("[ERROR] Passwords do not match. Host not added.")
            return

    hosts[name] = {"hostname": hostname, "user": user, "port": port}
    if identity:
        hosts[name]["identity"] = identity
    if password:
        hosts[name]["password"] = password

    save_config()
    print(f"[*] Host '{name}' added!")

def remove_host():
    list_hosts()
    name = prompt("Shortcut name to remove").strip()
    if name in hosts:
        del hosts[name]
        save_config()
        print(f"[*] Host '{name}' removed!")
    else:
        print(f"[ERROR] Host '{name}' not found.")

def ensure_local_key(key_path=DEFAULT_KEY_PATH):
    # Return path to private key; generate if missing
    key_pub = key_path + ".pub"
    if os.path.exists(key_path) and os.path.exists(key_pub):
        print(f"[*] Found existing key: {key_path}")
        return key_path
    if args.no_ask:
        print("[ERROR] No local key and --no-ask specified. Can't generate key.")
        return None
    print(f"[*] No key found at {key_path}. Generating new ed25519 keypair (no passphrase recommended for automation).")
    try:
        subprocess.run(["ssh-keygen", "-t", "ed25519", "-f", key_path], check=True)
        return key_path
    except subprocess.CalledProcessError:
        print("[ERROR] ssh-keygen failed. Make sure OpenSSH is installed.")
        return None

def copy_key_to_host(name):
    """Try to copy public key to remote host. Requires password once (or existing key auth)."""
    if name not in hosts:
        print(f"[ERROR] Host '{name}' not found.")
        return False
    info = hosts[name]
    user = info["user"]
    hostname = info["hostname"]
    port = str(info.get("port", 22))
    identity = info.get("identity", None)

    key_path = ensure_local_key()
    if not key_path:
        return False
    pub_key = key_path + ".pub"
    if not os.path.exists(pub_key):
        print("[ERROR] Public key not found after generation.")
        return False

    # Use ssh-copy-id if available
    if SSH_COPY_ID:
        cmd = ["ssh-copy-id", "-i", pub_key, "-p", port, f"{user}@{hostname}"]
        print("[*] Running ssh-copy-id (will prompt for password if needed)...")
        try:
            subprocess.run(cmd, check=True)
            print("[*] Public key copied successfully via ssh-copy-id.")
            # store identity path in config for convenience
            hosts[name]["identity"] = key_path
            save_config()
            return True
        except subprocess.CalledProcessError:
            print("[WARN] ssh-copy-id failed. Trying manual fallback.")
    else:
        print("[*] ssh-copy-id not found; using manual fallback.")

    # Manual fallback: cat pubkey and append to remote authorized_keys via ssh.
    with open(pub_key, "r") as f:
        pub = f.read().strip()

    # If the user stored password in config and sshpass exists, use sshpass to provide password non-interactively.
    pw = info.get("password")
    if pw and SSHPASS:
        remote_cmd = f"mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '{pub}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
        cmd = ["sshpass", "-p", pw, "ssh", "-p", port, f"{user}@{hostname}", remote_cmd]
        try:
            subprocess.run(cmd, check=True)
            print("[*] Public key appended to remote authorized_keys using sshpass.")
            hosts[name]["identity"] = key_path
            save_config()
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] Manual fallback with sshpass failed.")
            return False
    else:
        # Interactive ssh to append pubkey (will prompt for password)
        print("[*] Please enter the remote account password when prompted to append the public key.")
        remote_cmd = f"mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
        try:
            # open ssh and feed pub key via stdin
            ssh_proc = subprocess.Popen(["ssh", "-p", port, f"{user}@{hostname}", remote_cmd], stdin=subprocess.PIPE)
            ssh_proc.communicate((pub + "\n").encode())
            if ssh_proc.returncode == 0:
                print("[*] Public key appended to remote authorized_keys (interactive).")
                hosts[name]["identity"] = key_path
                save_config()
                return True
            else:
                print("[ERROR] Interactive key append failed (ssh returned non-zero).")
                return False
        except Exception as e:
            print("[ERROR] Exception while trying manual key append:", e)
            return False

def connect_host(name):
    if name not in hosts:
        print(f"[ERROR] Host '{name}' not found in saved hosts.")
        sys.exit(1)
    info = hosts[name]
    user = args.user or info["user"]
    hostname = info["hostname"]
    port = args.port or info.get("port", 22)
    identity = args.identity or info.get("identity")
    password = info.get("password")

    cmd = []
    use_sshpass = False
    if identity:
        # use explicit identity
        cmd = ["ssh", "-i", identity, "-p", str(port), f"{user}@{hostname}"]
    elif password and SSHPASS:
        # use sshpass to pass password (insecure)
        use_sshpass = True
        cmd = ["sshpass", "-p", password, "ssh", "-p", str(port), f"{user}@{hostname}"]
    else:
        cmd = ["ssh", "-p", str(port), f"{user}@{hostname}"]

    # If additional args were passed after --host, allow calling arbitrary remote command
    # If user invoked script like: ssh.py --host name ls -la  (argparse stops at known args by default)
    # We will allow remaining args via sys.argv parsing
    # build remote command suffix (anything after the host name)
    # Find index of host in argv to capture trailing args
    trailing = []
    if "--host" in sys.argv:
        try:
            idx = sys.argv.index("--host")
            if len(sys.argv) > idx + 1 and sys.argv[idx + 1] == name:
                # anything after that position are trailing args
                trailing = sys.argv[idx + 2 :]
        except ValueError:
            trailing = []

    if trailing:
        remote_cmd = " ".join([subprocess.list2cmdline(trailing)])
        # If using sshpass include the remote command in the ssh invocation
        if use_sshpass:
            cmd += [remote_cmd]
        else:
            cmd += [remote_cmd]

    print(f"[*] Connecting to {user}@{hostname}:{port} {'with identity ' + identity if identity else ''} ...")
    try:
        subprocess.run(cmd)
    except FileNotFoundError as e:
        print("[ERROR] Failed to run SSH command. Is ssh/sshpass installed?", e)
        sys.exit(1)

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

if args.setup_key:
    success = copy_key_to_host(args.setup_key)
    if success:
        print(f"[*] Key setup complete for host '{args.setup_key}'. You should be able to SSH without a password.")
    else:
        print(f"[ERROR] Key setup failed for host '{args.setup_key}'. See messages above.")
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
    choice = prompt(f"Select host [1-{len(hosts)}]")
    if not choice or not choice.isdigit() or not (1 <= int(choice) <= len(hosts)):
        print("[ERROR] Invalid choice")
        sys.exit(1)
    selected = list(hosts.keys())[int(choice)-1]
    connect_host(selected)

