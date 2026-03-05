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
# This enhances the show_status function with a visual progress bar.
def show_status(sp):
    curr = sp.current_playback()
    if not curr or not curr.get("item"):
        console.print("[yellow]⏹️ Nothing playing[/yellow]")
        return

    track = curr["item"]
    artists = ", ".join([a["name"] for a in track["artists"]])
    ms = curr["progress_ms"]
    total = track["duration_ms"]

    console.print(f"\n[bold green]▶️ {track['name']}[/bold green] - {artists}")
    
    with Progress(transient=True) as progress:
        task = progress.add_task("[cyan]Progress", total=total)
        progress.update(task, completed=ms)
    
    time_fmt = lambda m: f"{m//60000}:{(m%60000)//1000:02d}"
    console.print(f"   {time_fmt(ms)} / {time_fmt(total)} | 🔊 {curr['device']['name']}")
# This allows for more robust device switching and filtering.
def get_active_device(sp, requested_name=None):
    devices = sp.devices()["devices"]
    if not devices:
        console.print("[bold red]❌ No active Spotify devices found.[/bold red]")
        sys.exit(1)

    if requested_name:
        match = next((d for d in devices if requested_name.lower() in d["name"].lower()), None)
        if match: return match["id"]
    
    active = next((d for d in devices if d["is_active"]), devices[0])
    return active["id"]
# Added a cleaner search handler that returns URIs for playback.
def search_and_play(sp, query, device_id):
    console.print(f"[bold blue]🔍 Searching for:[/bold blue] {query}")
    results = sp.search(q=query, type="track", limit=5)
    
    if not results['tracks']['items']:
        console.print("[red]No results found.[/red]")
        return

    track = results['tracks']['items'][0]
    sp.start_playback(device_id=device_id, uris=[track['uri']])
    console.print(f"[green]Playing:[/green] {track['name']} by {track['artists'][0]['name']}")
# Boilerplate for command parsing and execution flow.
def main():
    sp = get_spotify_client()
    # Assume args are parsed here in a real scenario
    # This is a simplified block for commit testing
    dev_id = get_active_device(sp)
    show_status(sp)

if __name__ == "__main__":
    main()
