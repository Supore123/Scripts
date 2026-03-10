# JYScripts

A personal collection of shell and Python scripts that live in `~/Scripts` and get installed as global `jy`-prefixed commands. The idea is simple: things I run regularly that aren't worth typing out in full or remembering the flags for. Bluetooth, music, SSH shortcuts, system info, disk analysis, notes syncing, and a few other bits.

Everything installs to `/usr/local/bin` so any command is available anywhere in the terminal without needing a path.

---

## Installation

**1. Clone the repo**

```bash
git clone https://github.com/Supore123/Scripts.git ~/Scripts
cd ~/Scripts
```

**2. Install dependencies**

The installer handles apt packages, pip packages, symlinks, and udev rules. It also tells you what needs manual setup (conda, Spotify credentials, etc.) rather than silently skipping things.

```bash
chmod +x jyinstall.sh && ./jyinstall.sh
```

After it finishes, check the summary at the bottom — anything marked `[!]` needs a manual step.

**3. Install the scripts to PATH**

```bash
sudo ./update.sh
```

This copies every `.sh` and `.py` file in `~/Scripts` to `/usr/local/bin` with the `jy` prefix, sets permissions, and removes any old commands that no longer have a source file. Re-run it any time you add or rename a script.

**4. Reload your shell**

```bash
source ~/.bashrc
```

---

## Getting help

```bash
jy
```

Lists every installed command with a one-line description. That's it.

For a specific command:

```bash
jyhelper music
jyhelper ssh
jyhelper airpods
```

---

## Demo

```
$ jy

╔═══════════════════════════════════════╗
║     📚 Available jy Commands          ║
╚═══════════════════════════════════════╝

  • jyairpods       Connect/disconnect AirPods and show battery
  • jybright        Adjust screen brightness
  • jychat          Natural language assistant for running jy commands
  • jydiskbloat     Disk usage analyser with colour-coded output
  • jyenv           Conda environment manager
  • jyetym          Etymology lookup
  • jyfind          Interactive file finder (fzf)
  • jygit           GitHub dashboard — repos, commits, PRs, languages
   jymatrix        System diagnostic boot screen
  • jymusic         Spotify controls from the terminal
  • jynetcheck      Network speed and connectivity test
  • jynotes         Auto-commit and push notes repo
  • jyremind        Desktop notification reminders
  • jyssh           SSH connection manager with saved shortcuts
  • jysysinfo       CPU, RAM, disk, GPU, battery at a glance
  • jytranslate     Translate text via Google Translate
  • jyuno           Compile and flash Arduino sketches
  • jyesp32         Compile and flash ESP32 sketches
  • jyvpn           Toggle ProtonVPN and open/close Chrome incognito
  • jyweather       Current weather for any city

💡 For detailed help: jyhelper <command>
💬 Or chat with me: jychat
```

```
$ jysysinfo

🖥️  System Information (High Precision)
----------------------------------------
Hostname:    jon-desktop
Uptime:      up 3 hours, 12 minutes
CPU Cores:   12
CPU Load:    0.45, 0.61, 0.72
RAM:         6.24G used / 15.53G total (9.29G free)
Disk (root): 48.31G used / 233.47G total | 173.04G left (21% used)
Battery:     84% (discharging, 8.2 W, 3 hours 40 minutes) ████████████████░░░░
Local IP:    192.168.1.45
Public IP:   82.x.x.x
----------------------------------------
✅ Done
```

```
$ jyairpods

[*] Powering on Bluetooth...
[*] Device already paired/trusted.
[*] Connecting to AirPods (0C:53:B7:8E:4A:62)...
[*] Connected successfully!
[*] Left AirPod: 78%
[*] Right AirPod: 81%
[*] Case: 100%
[*] Setting bluez_sink.0c_53_b7_8e_4a_62 as default audio output.
[*] Done!
```

```
$ jychat
You: connect airpods and then play discovery by daft punk
Bot: [1/2] Running airpods...
     ✅ airpods completed
     [2/2] Running music...
     ✅ Playing: Discovery by Daft Punk
```

---

## Adding your own commands

1. Write a script in `~/Scripts`, named without the `jy` prefix (e.g. `myscript.sh`)
2. Add a `# DESC:` comment at the top so it shows up in `jyhelp`
3. Run `sudo jyupdate` to install it

```bash
#!/usr/bin/env bash
# DESC: Does something useful
# EXAMPLE: jymyscript

echo "hello"
```

That's all it takes. The update script handles the rest.

---

## Notes

- Scripts are designed for Linux (tested on Kubuntu / KDE Plasma, X11)
- Python scripts require Python 3
- `jymusic` requires Spotify credentials set as environment variables (`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`)
- `jygit` requires a `GITHUB_TOKEN` environment variable
- `jyenv` requires conda (Miniconda or Anaconda)
- `jyvpn` requires the ProtonVPN CLI

See `jyinstall.sh` for the full dependency breakdown and setup instructions.•
