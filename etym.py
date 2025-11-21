#!/usr/bin/env python3
# DESC: Etymology lookup tool with robust extraction, table output, colors, caching, multi-word support, offline mode, and TUI.
# ARG: WORD                Word(s) to look up (default positional argument)
# ARG: --word WORD         Optional explicit word
# ARG: --file FILE         Read multiple words from a file
# ARG: --json              Output in JSON format
# ARG: --raw               Print raw HTML
# ARG: --offline           Use cache only, no network
# ARG: --no-color          Disable color output
# ARG: --no-pretty         Disable text prettification
# ARG: --interactive       TUI selection mode
# ARG: --cache             Use and update local cache (~/.jyetym.json)

import argparse
import urllib.request
import urllib.error
import json
import os
import re
import html
import sys
import time
from shutil import get_terminal_size

CACHE_PATH = os.path.expanduser("~/.jyetym.json")

# -------------------------
# Load cache
# -------------------------
if not os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "w") as f:
        json.dump({}, f)

with open(CACHE_PATH) as f:
    cache = json.load(f)

# -------------------------
# Color helpers
# -------------------------
def supports_color():
    return sys.stdout.isatty()

def c(text, color=None):
    if not color_enabled:
        return text
    colors = {
        "green": "\033[92m",
        "cyan":  "\033[96m",
        "yellow": "\033[93m",
        "red":   "\033[91m",
        "bold":  "\033[1m",
        "reset": "\033[0m",
    }
    return colors.get(color, "") + text + colors["reset"]

# -------------------------
# CLI
# -------------------------
parser = argparse.ArgumentParser(description="Fetch etymology for word(s) and display in a table.")
parser.add_argument("words", nargs="*", help="Words to look up")
parser.add_argument("--word", type=str, help="Word to look up (legacy)")
parser.add_argument("--file", type=str, help="Read list of words from file")
parser.add_argument("--json", action="store_true", help="Print JSON output")
parser.add_argument("--raw", action="store_true", help="Print raw HTML")
parser.add_argument("--offline", action="store_true", help="Use cache only, no network")
parser.add_argument("--no-color", action="store_true", help="Disable color output")
parser.add_argument("--no-pretty", action="store_true", help="Disable pretty formatting")
parser.add_argument("--interactive", action="store_true", help="Interactive selection mode")
parser.add_argument("--cache", action="store_true", help="Use and update local cache")

args = parser.parse_args()
color_enabled = supports_color() and not args.no_color

# -------------------------
# Helpers
# -------------------------
def save_cache():
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=4)

def fetch_html(word):
    if args.offline:
        return None
    url = f"https://www.etymonline.com/word/{word}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=6) as r:
            return r.read().decode("utf-8")
    except:
        return None

def extract_etym(html_text):
    """
    Robust etymology extractor. Removes advertisements and premium messages.
    """
    # Remove typical Etymonline ads / premium text
    html_text = re.sub(r'Advertisement.*?Premium Member', '', html_text, flags=re.DOTALL)
    html_text = re.sub(r'Want to remove ads\?.*?Log in', '', html_text, flags=re.DOTALL)

    # Strategy 1: <section> with 'etymology'
    section_matches = re.findall(r'<section[^>]*>(.*?)</section>', html_text, re.DOTALL)
    for block in section_matches:
        if "Etymology" in block or "etymology" in block or "origin" in block.lower():
            cleaned = re.sub(r'<[^>]+>', '', block)
            cleaned = html.unescape(cleaned).strip()
            if len(cleaned.split()) > 4:
                return cleaned

    # Strategy 2: fallback: <p> containing key etymology terms
    p_matches = re.findall(r'<p>(.*?)</p>', html_text, re.DOTALL)
    for p in p_matches:
        if any(k in p.lower() for k in ["from ", "cognate", "proto-", "old ", "latin", "greek"]):
            cleaned = re.sub(r'<[^>]+>', '', p)
            return html.unescape(cleaned).strip()

    return None

def pretty(text):
    text = re.sub(r'\s+', ' ', text)
    return text.replace(". ", ".\n")

def lookup(word):
    w = word.lower()
    if args.cache and w in cache:
        return cache[w]

    raw = fetch_html(w)
    if raw is None:
        return None

    if args.raw:
        print(raw)
        return None

    et = extract_etym(raw)
    if et:
        cache[w] = {
            "etymology": et,
            "timestamp": time.time()
        }
        save_cache()
    return cache.get(w)

def load_words():
    words = []
    words.extend(args.words)
    if args.word:
        words.append(args.word)
    if args.file:
        if not os.path.exists(args.file):
            print(c("[ERROR] File not found.", "red"))
            sys.exit(1)
        with open(args.file) as f:
            for line in f:
                w = line.strip()
                if w:
                    words.append(w)
    if not words:
        print(c("[ERROR] No words supplied.", "red"))
        sys.exit(1)
    return words

def interactive_select(words):
    print(c("Select a word:\n", "yellow"))
    for i, w in enumerate(words, 1):
        print(f"{i}. {w}")
    choice = input("\nChoice: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(words)):
        print(c("[ERROR] Invalid choice.", "red"))
        sys.exit(1)
    return [words[int(choice)-1]]

def print_table(results):
    # Determine column width
    term_width = max(len(w) for w in results.keys()) + 4
    max_width = get_terminal_size((80, 20)).columns
    for w, data in results.items():
        et_text = data["etymology"]
        if not args.no_pretty:
            et_text = pretty(et_text)
        lines = et_text.split("\n")
        print(c("=" * max_width, "cyan"))
        print(c(f"{w.upper():<{term_width}} | {lines[0]}", "green"))
        for line in lines[1:]:
            print(f"{'':<{term_width}} | {line}")
    print(c("=" * max_width, "cyan"))

# -------------------------
# Main
# -------------------------
words = load_words()
if args.interactive and len(words) > 1:
    words = interactive_select(words)

results = {}
for w in words:
    data = lookup(w)
    if not data:
        print(c(f"[!] No etymology found for '{w}'.", "red"))
        continue
    results[w] = data

if args.json:
    print(json.dumps(results, indent=4))
else:
    print_table(results)
