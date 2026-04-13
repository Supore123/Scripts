#!/usr/bin/env python3
# DESC: Display a detailed GitHub dashboard with repo stats, activity, commits, PRs, issues, language breakdown, and top 5 repos
# TAG: github, stats, dashboard
# ARG: None - uses your GitHub token from environment
# EXAMPLE: jy github

import os
import requests
from collections import Counter
from datetime import datetime
from rich.console import Console
from rich.table import Table

# -----------------------------
# Config
# -----------------------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("❌ Please set your GITHUB_TOKEN environment variable")
    exit(1)

API_BASE = "https://api.github.com"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

console = Console()

# -----------------------------
# Helper functions
# -----------------------------
def get_user_info():
    r = requests.get(f"{API_BASE}/user", headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_all_pages(url, params=None):
    results = []
    page = 1
    while True:
        p = params.copy() if params else {}
        p.update({"per_page": 100, "page": page})
        r = requests.get(url, headers=HEADERS, params=p)
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        results.extend(data)
        page += 1
    return results

def summarize_repos(repos):
    total = len(repos)
    public = sum(1 for r in repos if not r["private"])
    private = total - public
    forks = sum(1 for r in repos if r["fork"])
    stars = sum(r["stargazers_count"] for r in repos)
    languages = Counter()
    for r in repos:
        if r["language"]:
            languages[r["language"]] += 1
    return total, public, private, forks, stars, languages

def get_recent_activity(username):
    events = get_all_pages(f"{API_BASE}/users/{username}/events")
    commits = sum(1 for e in events if e["type"] == "PushEvent")
    prs_opened = sum(
        1 for e in events
        if e["type"] == "PullRequestEvent" and e["payload"]["action"] == "opened"
    )
    prs_merged = sum(
    1 for e in events
    if e["type"] == "PullRequestEvent" 
    and e["payload"].get("action") == "closed" 
    and e["payload"].get("pull_request", {}).get("merged") is True
    )
    issues_opened = sum(
        1 for e in events
        if e["type"] == "IssuesEvent" and e["payload"]["action"] == "opened"
    )
    issues_commented = sum(
        1 for e in events if e["type"] == "IssueCommentEvent"
    )
    return commits, prs_opened, prs_merged, issues_opened, issues_commented

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    user_info = get_user_info()
    username = user_info["login"]
    repos = get_all_pages(f"{API_BASE}/user/repos")

    total, public, private, forks, stars, languages = summarize_repos(repos)
    commits, prs_opened, prs_merged, issues_opened, issues_commented = get_recent_activity(username)

    console.print(f"👤 GitHub Summary for: [bold]{username}[/bold]\n")

    # Repository summary
    repo_table = Table(title="Repositories")
    repo_table.add_column("Total", justify="right")
    repo_table.add_column("Public", justify="right")
    repo_table.add_column("Private", justify="right")
    repo_table.add_column("Forks", justify="right")
    repo_table.add_column("Stars", justify="right")
    repo_table.add_row(str(total), str(public), str(private), str(forks), str(stars))
    console.print(repo_table)

    # Language breakdown
    lang_table = Table(title="Language Breakdown")
    lang_table.add_column("Language")
    lang_table.add_column("Repos", justify="right")
    for lang, count in languages.most_common():
        lang_table.add_row(lang, str(count))
    console.print(lang_table)

    # Recent activity
    activity_table = Table(title="Recent Activity (last ~100 events)")
    activity_table.add_column("Metric")
    activity_table.add_column("Count", justify="right")
    activity_table.add_row("Commits pushed", str(commits))
    activity_table.add_row("PRs opened", str(prs_opened))
    activity_table.add_row("PRs merged", str(prs_merged))
    activity_table.add_row("Issues opened", str(issues_opened))
    activity_table.add_row("Issues commented", str(issues_commented))
    console.print(activity_table)

    # Top 5 repos by stars
    top_repos = sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)[:5]
    top_table = Table(title="Top 5 Repositories by Stars")
    top_table.add_column("Repo")
    top_table.add_column("Stars", justify="right")
    top_table.add_column("Forks", justify="right")
    top_table.add_column("Last Updated")
    for r in top_repos:
        updated = datetime.strptime(r["updated_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        top_table.add_row(r["name"], str(r["stargazers_count"]), str(r["forks_count"]), updated)
    console.print(top_table)

