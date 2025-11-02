#!/usr/bin/env python3
"""
JYmusic.py — Spotify CLI controller
- Fully CLI-friendly: arguments override cached state
- Automatically resumes last device/playlist if no args
- Optional interactive selection if nothing is found
- CLI song picker: --song "track name"
"""

import os, sys, json, argparse
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

CACHE_FILE = os.path.expanduser("~/.cache/JYmusic_state.json")
CACHE_PATH = os.path.expanduser("~/.cache/JYmusic_cache")

# Environment credentials
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

if not CLIENT_ID or not CLIENT_SECRET:
    print("[ERROR] Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in environment.")
    sys.exit(1)

# -------------------------
# CLI Arguments
# -------------------------
parser = argparse.ArgumentParser(description="Spotify CLI controller")
parser.add_argument("--resume", action="store_true", help="Resume last device/playlist automatically")
parser.add_argument("--device", type=str, help="Device name")
parser.add_argument("--playlist", type=str, help="Playlist name")
parser.add_argument("--song", type=str, help="Play a specific song")
parser.add_argument("--volume", type=int, help="Volume 0-100")
parser.add_argument("--shuffle", action="store_true")
parser.add_argument("--play", action="store_true")
parser.add_argument("--pause", action="store_true")
parser.add_argument("--next", action="store_true")
parser.add_argument("--previous", action="store_true")
parser.add_argument("--status", action="store_true")
args = parser.parse_args()

# -------------------------
# Spotify authentication
# -------------------------
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state,playlist-read-private",
    cache_path=CACHE_PATH
))

# -------------------------
# Load last state
# -------------------------
state = {}
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE) as f:
            state = json.load(f)
    except Exception:
        state = {}

# -------------------------
# Determine if we're in CLI mode (any args provided)
# -------------------------
cli_mode = any([
    args.device, args.playlist, args.song, args.volume is not None,
    args.shuffle, args.play, args.pause, args.next, args.previous,
    args.status, args.resume
])

# -------------------------
# Select device
# -------------------------
devices = sp.devices()["devices"]
if not devices:
    print("[ERROR] No active Spotify devices. Open Spotify somewhere.")
    sys.exit(1)

device = None
if args.device:
    # Explicit device specified
    device = next((d for d in devices if args.device.lower() in d["name"].lower()), None)
    if not device:
        print(f"[ERROR] Device '{args.device}' not found.")
        sys.exit(1)
elif args.resume and state.get("device_id"):
    # Resume with cached device
    device = next((d for d in devices if d["id"] == state["device_id"]), None)
    if not device:
        print("[WARNING] Cached device not available, using active device.")
        device = next((d for d in devices if d["is_active"]), devices[0])
elif cli_mode:
    # CLI mode but no device specified: use active or first available
    device = next((d for d in devices if d["is_active"]), devices[0])
else:
    # Interactive mode: prompt user
    print("[*] Available devices:")
    for i, d in enumerate(devices, start=1):
        status = "ACTIVE" if d["is_active"] else "INACTIVE"
        print(f"{i}. {d['name']} ({d['type']}) - {status}")
    choice = input(f"Select device [1-{len(devices)}] (default 1): ").strip()
    choice = choice or "1"
    device = devices[int(choice)-1]

device_id = device["id"]

# -------------------------
# Select playlist
# -------------------------
playlist_uri = None
playlists = []

# Only fetch playlists if needed
if args.playlist or (not cli_mode) or (args.resume and not args.song):
    results = sp.current_user_playlists(limit=50)
    while results:
        playlists.extend(results["items"])
        if results["next"]:
            results = sp.next(results)
        else:
            break

if args.playlist:
    # Explicit playlist specified
    match = [p for p in playlists if args.playlist.lower() in p["name"].lower()]
    if match:
        playlist_uri = match[0]["uri"]
    else:
        print(f"[ERROR] Playlist '{args.playlist}' not found.")
        sys.exit(1)
elif args.resume and state.get("playlist_uri") and not args.song:
    # Resume with cached playlist
    playlist_uri = state["playlist_uri"]
elif not cli_mode and not args.song:
    # Interactive mode: prompt for playlist
    print("\n[*] Your playlists:")
    for i, p in enumerate(playlists, start=1):
        print(f"{i}. {p['name']} ({p['tracks']['total']} tracks)")
    choice = input(f"Select playlist [1-{len(playlists)}] (or blank to skip): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(playlists):
        playlist_uri = playlists[int(choice)-1]["uri"]

# -------------------------
# Execute commands
# -------------------------
if args.volume is not None:
    sp.volume(args.volume, device_id=device_id)
    print(f"[*] Volume set to {args.volume}%")

if args.shuffle:
    sp.shuffle(True, device_id=device_id)
    print("[*] Shuffle enabled")

# Handle song search first (takes priority)
if args.song:
    results = sp.search(q=args.song, type="track", limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        uri = track['uri']
        sp.start_playback(device_id=device_id, uris=[uri])
        print(f"[*] Playing track: {track['name']} - {track['artists'][0]['name']}")
    else:
        print(f"[ERROR] Track '{args.song}' not found.")
        sys.exit(1)
elif args.play:
    # Start playback with playlist if available
    if playlist_uri:
        sp.start_playback(device_id=device_id, context_uri=playlist_uri)
        print("[*] Playback started")
    else:
        # Resume current playback
        sp.start_playback(device_id=device_id)
        print("[*] Playback resumed")
elif args.pause:
    sp.pause_playback(device_id=device_id)
    print("[*] Playback paused")

if args.next:
    sp.next_track(device_id=device_id)
    print("[*] Skipped to next track")

if args.previous:
    sp.previous_track(device_id=device_id)
    print("[*] Skipped to previous track")

if args.status:
    current = sp.current_playback()
    if current and current.get("item"):
        track = current["item"]
        artists = ", ".join([a["name"] for a in track["artists"]])
        is_playing = current.get("is_playing", False)
        status = "Playing" if is_playing else "Paused"
        print(f"[*] {status}: {track['name']} - {artists}")
        print(f"[*] Device: {current['device']['name']}")
    else:
        print("[*] No track currently playing")

# -------------------------
# Save state (only if we made changes)
# -------------------------
if device_id or playlist_uri:
    state = {
        "device_id": device_id,
        "playlist_uri": playlist_uri
    }
    with open(CACHE_FILE, "w") as f:
        json.dump(state, f)

print("[*] Done")
