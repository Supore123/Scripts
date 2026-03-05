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
