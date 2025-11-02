#!/usr/bin/env python3
"""
JYmusic.py — Interactive Spotify player using Spotipy
Allows selecting the device and playlist to play.
"""

import os
import sys
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# -------------------------
# Environment variables
# -------------------------
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
CACHE_PATH = os.path.expanduser("~/.cache/JYmusic_cache")

if not CLIENT_ID or not CLIENT_SECRET:
    print("[ERROR] Spotify CLIENT_ID or CLIENT_SECRET not set in environment.")
    sys.exit(1)

# -------------------------
# Authenticate with Spotify API
# -------------------------
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state,playlist-read-private",
    cache_path=CACHE_PATH
))

# -------------------------
# List available devices
# -------------------------
devices = sp.devices()["devices"]
if not devices:
    print("[ERROR] No active Spotify devices found. Open Spotify on a device first.")
    sys.exit(1)

print("[*] Available Spotify devices:")
for i, d in enumerate(devices, start=1):
    status = "ACTIVE" if d["is_active"] else "INACTIVE"
    print(f"{i}. {d['name']} ({d['type']}) - {status}")

# Prompt user to choose a device
while True:
    choice = input(f"Select device [1-{len(devices)}] (default 1): ").strip()
    if choice == "":
        choice = "1"
    if choice.isdigit() and 1 <= int(choice) <= len(devices):
        device = devices[int(choice) - 1]
        break
    print("Invalid choice. Try again.")

print(f"[*] Using device: {device['name']} ({device['type']})")

# -------------------------
# List available playlists
# -------------------------
playlists = []
results = sp.current_user_playlists(limit=50)
while results:
    playlists.extend(results["items"])
    if results["next"]:
        results = sp.next(results)
    else:
        break

if playlists:
    print("\n[*] Your Playlists:")
    for i, p in enumerate(playlists, start=1):
        print(f"{i}. {p['name']} ({p['tracks']['total']} tracks)")

    while True:
        choice = input(f"Select playlist to play [1-{len(playlists)}] (or leave blank to skip): ").strip()
        if choice == "":
            playlist_uri = None
            break
        if choice.isdigit() and 1 <= int(choice) <= len(playlists):
            playlist_uri = playlists[int(choice) - 1]["uri"]
            break
        print("Invalid choice. Try again.")
else:
    print("[*] No playlists found in your account.")
    playlist_uri = None

# -------------------------
# Start playback
# -------------------------
if playlist_uri:
    sp.start_playback(device_id=device["id"], context_uri=playlist_uri)
    print(f"[*] Playing playlist: {playlist_uri}")
else:
    print("[*] Ready to control playback manually on the selected device.")
