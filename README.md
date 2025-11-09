# JYScripts

A curated collection of shell and Python scripts used for custom CLI commands on Linux.

## Available Commands

Each script is prefixed with `JY` when installed.

### JYairpods
`airpods.sh` — Automatically connect and set the audio sink to AirPods (or another Bluetooth audio device). Displays battery level.

### JYmusic
`music.py` — Control your music player from the command line.

Examples:
- Resume the last session:
JYmusic --resume --play

sql
Copy code
- Play a specific song without prompts:
JYmusic --song "Bohemian Rhapsody"

css
Copy code
- Play a playlist on a specific device:
JYmusic --device "Kitchen Speaker" --playlist "Workout" --play

diff
Copy code
- Quick controls:
JYmusic --next
JYmusic --volume 50
JYmusic --pause

pgsql
Copy code
- Interactive mode (no arguments):
JYmusic

markdown
Copy code

### JYsysinfo
`sysinfo.sh` — Display detailed system information: CPU, RAM, disk usage, GPU, network status, uptime.

### JYupdate
`update.sh` — Install (or update) all the scripts in this folder to `/usr/local/bin` with the `JY` prefix, making them globally available.

Other scripts in the repository include: `checkhost.sh`, `define.sh`, `env.sh`, `find.sh`, `git.py`, `help.sh`, `helper.sh`, `myip.sh`, `network.py`, `notes.sh`, `remind.sh`, `ssh.py`, `translate.sh`, `weather.sh`.

## Getting Started

1. Clone the repository:
git clone https://github.com/Supore123/Scripts.git

csharp
Copy code
2. Change into the directory:
cd Scripts

pgsql
Copy code
3. Run the update install script to add all commands to PATH:
sudo ./update.sh

markdown
Copy code
This will copy or symlink each script to `/usr/local/bin` prefixed with `JY`.

4. Use any of the commands from anywhere in your shell.

## Dependencies & Requirements

- Linux environment.
- Bash (for shell scripts) or Python 3 (for `.py` scripts).
- Specific commands may require: Bluetooth setup, a supported music player CLI, network tools, etc.
- Permissions: installation script may require `sudo` to write to `/usr/local/bin`.

## Customising & Extending

- Inspect each script and modify paths or naming conventions to match your workflow.
- To add a new command:
1. Write a script, follow the naming convention, test locally.
2. Add it to the repository and update the `update.sh` installer if needed.
- Consider adding shell completions, man-pages, or alias support for smoother usage.

## Author & Licence

Created and maintained by **Supore123**.

You’re free to use and adapt these scripts for personal workflow. No formal license is included — treat it as permissive. Contribution guidelines or a LICENSE file may be added in future.
