#!/usr/bin/env python3
"""
JYmusic — Beautiful Spotify CLI controller

Quick examples:
  jymusic                           # Resume last session & show status
  jymusic "bohemian rhapsody"       # Search and play song
  jymusic next                      # Skip track
  jymusic vol 80                    # Set volume
  jymusic -p "chill vibes"          # Play playlist
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
    print("❌ Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in environment.")
    sys.exit(1)

# -------------------------
# Enhanced CLI Arguments
# -------------------------
parser = argparse.ArgumentParser(
    description="🎵 Spotify CLI controller",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  %(prog)s                          Resume & show status
  %(prog)s "rick astley"            Search and play
  %(prog)s next                     Skip to next track
  %(prog)s prev                     Previous track
  %(prog)s pause                    Pause playback
  %(prog)s play                     Resume playback
  %(prog)s vol 75                   Set volume to 75%%
  %(prog)s shuffle                  Toggle shuffle
  %(prog)s -p "workout mix"         Play playlist
  %(prog)s -d "Kitchen"             Select device
  %(prog)s --playlists              Browse and select playlist
    """
)

# Positional argument for quick commands
parser.add_argument("command", nargs="*", help="Quick command: next/prev/pause/play/shuffle or song search")

# Flags with short aliases
parser.add_argument("-d", "--device", type=str, help="Device name")
parser.add_argument("-p", "--playlist", type=str, help="Playlist name")
parser.add_argument("-s", "--song", type=str, help="Search for a specific song")
parser.add_argument("-v", "--volume", type=int, help="Volume 0-100")
parser.add_argument("--shuffle", action="store_true", help="Enable shuffle")
parser.add_argument("--status", action="store_true", help="Show current status")
parser.add_argument("--playlists", action="store_true", help="Show and select from playlists")
parser.add_argument("-i", "--interactive", action="store_true", help="Force interactive mode")

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
# Parse quick commands
# -------------------------
command_str = " ".join(args.command).lower() if args.command else ""
quick_action = None
search_query = None

if command_str:
    if command_str in ["next", "n", "skip"]:
        quick_action = "next"
    elif command_str in ["prev", "previous", "back", "b"]:
        quick_action = "prev"
    elif command_str in ["pause", "stop"]:
        quick_action = "pause"
    elif command_str in ["play", "resume", "start"]:
        quick_action = "play"
    elif command_str in ["shuffle", "shuf", "random"]:
        quick_action = "shuffle"
    elif command_str.startswith("vol"):
        # Extract volume: "vol 80" or "volume 80"
        parts = command_str.split()
        if len(parts) > 1 and parts[1].isdigit():
            args.volume = int(parts[1])
    else:
        # Treat as song search
        search_query = " ".join(args.command)

# Override with explicit song flag
if args.song:
    search_query = args.song

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
# Determine mode
# -------------------------
cli_mode = any([
    args.device, args.playlist, search_query, args.volume is not None,
    args.shuffle, quick_action, args.status, args.playlists
]) and not args.interactive

# -------------------------
# Helper: Show status
# -------------------------
def show_status():
    current = sp.current_playback()
    if current and current.get("item"):
        track = current["item"]
        artists = ", ".join([a["name"] for a in track["artists"]])
        is_playing = current.get("is_playing", False)
        progress_ms = current.get("progress_ms", 0)
        duration_ms = track.get("duration_ms", 0)

        # Format time
        progress_min = progress_ms // 60000
        progress_sec = (progress_ms % 60000) // 1000
        duration_min = duration_ms // 60000
        duration_sec = (duration_ms % 60000) // 1000

        status_icon = "▶️" if is_playing else "⏸️"
        print(f"\n{status_icon}  {track['name']}")
        print(f"   {artists}")
        print(f"   {progress_min}:{progress_sec:02d} / {duration_min}:{duration_sec:02d}")
        print(f"   🔊 {current['device']['name']}")
        if current.get("shuffle_state"):
            print(f"   🔀 Shuffle on")
        return True
    else:
        print("⏹️  Nothing playing")
        return False

# -------------------------
# Select device
# -------------------------
devices = sp.devices()["devices"]
if not devices:
    print("❌ No active Spotify devices. Open Spotify somewhere.")
    sys.exit(1)

device = None
if args.device:
    device = next((d for d in devices if args.device.lower() in d["name"].lower()), None)
    if not device:
        print(f"❌ Device '{args.device}' not found.")
        sys.exit(1)
elif state.get("device_id"):
    device = next((d for d in devices if d["id"] == state["device_id"]), None)

if not device:
    if cli_mode:
        device = next((d for d in devices if d["is_active"]), devices[0])
    else:
        print("\n🔊 Available devices:")
        for i, d in enumerate(devices, start=1):
            status = "●" if d["is_active"] else "○"
            print(f"{i}. {status} {d['name']} ({d['type']})")
        choice = input(f"Select device [1-{len(devices)}] (default 1): ").strip()
        choice = choice or "1"
        device = devices[int(choice)-1]

device_id = device["id"]

# -------------------------
# Handle quick actions
# -------------------------
if quick_action == "next":
    sp.next_track(device_id=device_id)
    print("⏭️  Skipped")
    import time; time.sleep(0.5)  # Wait for Spotify to update
    show_status()
    sys.exit(0)
elif quick_action == "prev":
    sp.previous_track(device_id=device_id)
    print("⏮️  Previous")
    import time; time.sleep(0.5)
    show_status()
    sys.exit(0)
elif quick_action == "pause":
    sp.pause_playback(device_id=device_id)
    print("⏸️  Paused")
    sys.exit(0)
elif quick_action == "play":
    sp.start_playback(device_id=device_id)
    print("▶️  Playing")
    import time; time.sleep(0.5)
    show_status()
    sys.exit(0)
elif quick_action == "shuffle":
    current = sp.current_playback()
    current_shuffle = current.get("shuffle_state", False) if current else False
    sp.shuffle(not current_shuffle, device_id=device_id)
    print(f"🔀 Shuffle {'on' if not current_shuffle else 'off'}")
    sys.exit(0)

# -------------------------
# Volume control
# -------------------------
if args.volume is not None:
    sp.volume(args.volume, device_id=device_id)
    print(f"🔊 Volume: {args.volume}%")

# -------------------------
# Search and play song
# -------------------------
if search_query:
    print(f"🔍 Searching for: {search_query}")
    results = sp.search(q=search_query, type="track", limit=10)

    if results['tracks']['items']:
        tracks = results['tracks']['items']

        if len(tracks) == 1 or cli_mode:
            # Auto-play first result in CLI mode
            track = tracks[0]
            sp.start_playback(device_id=device_id, uris=[track['uri']])
            print(f"▶️  Playing: {track['name']} - {track['artists'][0]['name']}")
            import time; time.sleep(0.5)
            show_status()
        else:
            # Show options
            print(f"\n🎵 Found {len(tracks)} tracks:")
            for i, t in enumerate(tracks, start=1):
                artists = ", ".join([a["name"] for a in t["artists"]])
                album = t["album"]["name"]
                print(f"{i}. {t['name']} - {artists}")
                print(f"   ({album})")

            choice = input(f"\nSelect track [1-{len(tracks)}] (default 1): ").strip()
            choice = choice or "1"
            track = tracks[int(choice)-1]
            sp.start_playback(device_id=device_id, uris=[track['uri']])
            print(f"▶️  Playing: {track['name']}")
            import time; time.sleep(0.5)
            show_status()
    else:
        print(f"❌ No tracks found for '{search_query}'")
        sys.exit(1)

    # Save state and exit
    state = {"device_id": device_id, "playlist_uri": None}
    with open(CACHE_FILE, "w") as f:
        json.dump(state, f)
    sys.exit(0)

# -------------------------
# Playlist selection
# -------------------------
playlist_uri = None

if args.playlist or (not cli_mode and not search_query):
    results = sp.current_user_playlists(limit=50)
    playlists = []
    while results:
        playlists.extend(results["items"])
        if results["next"]:
            results = sp.next(results)
        else:
            break

    if args.playlist:
        match = [p for p in playlists if args.playlist.lower() in p["name"].lower()]
        if match:
            playlist_uri = match[0]["uri"]
            sp.start_playback(device_id=device_id, context_uri=playlist_uri)
            print(f"▶️  Playing playlist: {match[0]['name']}")
        else:
            print(f"❌ Playlist '{args.playlist}' not found.")
            sys.exit(1)
    elif not cli_mode:
        print("\n📚 Your playlists:")
        for i, p in enumerate(playlists[:20], start=1):  # Show top 20
            print(f"{i}. {p['name']} ({p['tracks']['total']} tracks)")

        choice = input(f"\nSelect playlist [1-{min(20, len(playlists))}] (or Enter to skip): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(playlists):
            playlist_uri = playlists[int(choice)-1]["uri"]
            sp.start_playback(device_id=device_id, context_uri=playlist_uri)
            print(f"▶️  Playing: {playlists[int(choice)-1]['name']}")

# -------------------------
# Shuffle if requested
# -------------------------
if args.shuffle:
    sp.shuffle(True, device_id=device_id)
    print("🔀 Shuffle enabled")

# -------------------------
# Show status (default behavior)
# -------------------------
if args.status or (not quick_action and not search_query and not args.playlist):
    show_status()

# -------------------------
# Save state
# -------------------------
state = {
    "device_id": device_id,
    "playlist_uri": playlist_uri
}
with open(CACHE_FILE, "w") as f:
    json.dump(state, f)
