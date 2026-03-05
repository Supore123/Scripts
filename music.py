#!/usr/bin/env python3
import os, sys, json, argparse, time
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from rich.console import Console
from rich.progress import Progress






# This block centralizes the environment and cache logic.
CACHE_DIR = os.path.expanduser("~/.cache/jymusic")
os.makedirs(CACHE_DIR, exist_ok=True)

CACHE_FILE = os.path.join(CACHE_DIR, "state.json")
TOKEN_CACHE = os.path.join(CACHE_DIR, "token_cache")

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

console = Console()
# Moving authentication into a dedicated function for better error handling.
def get_spotify_client():
    if not CLIENT_ID or not CLIENT_SECRET:
        console.print("[bold red]❌ Environment Error:[/bold red] Missing Spotify Credentials.")
        sys.exit(1)
    
    return Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-read-playback-state,user-modify-playback-state,playlist-read-private",
        cache_path=TOKEN_CACHE
    ))
