#!/usr/bin/env python3
"""
CodeCraft - GitHub Trending 自动抓取脚本
每周运行一次，更新明星项目数据
用法: python scripts/update_stars.py
"""
import urllib.request
import json
import re
import os
import sys
from datetime import datetime, timedelta, timezone


def github_request(url):
    """Fetch GitHub API JSON, using the Actions token when available."""
    headers = {
        "User-Agent": "CodeCraft/1.1",
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def recent_date(days=365):
    """Return a moving GitHub search date instead of a stale hard-coded year."""
    return (datetime.now(timezone.utc).date() - timedelta(days=days)).isoformat()

def fetch_trending(language="", since="weekly"):
    """Fetch trending repos from GitHub unofficial API"""
    url = f"https://api.github.com/search/repositories?q=stars:>100+pushed:>2025-01-01&sort=stars&order=desc&per_page=10"
    if language:
        url += f"+language:{language}"
    
    try:
        data = github_request(url)
        return data.get("items", [])
    except Exception as e:
        print(f"Error fetching trending: {e}")
        return []

def fetch_weekly_stars():
    """Get repos with most stars gained this week"""
    # Use GitHub search API to find recently created popular repos
    created_after = recent_date()
    queries = [
        f"stars:>500+created:>{created_after}+language:javascript",
        f"stars:>500+created:>{created_after}+language:python",
        f"stars:>500+created:>{created_after}+language:typescript",
    ]
    
    all_repos = []
    for q in queries:
        url = f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=3"
        try:
            data = github_request(url)
            all_repos.extend(data.get("items", []))
        except Exception as e:
            print(f"Error: {e}")
    
    # Deduplicate and sort by stars
    seen = set()
    unique = []
    for r in all_repos:
        if r["full_name"] not in seen:
            seen.add(r["full_name"])
            unique.append(r)
    
    unique.sort(key=lambda x: x["stargazers_count"], reverse=True)
    return unique[:6]

def generate_stars_js(repos):
    """Generate JavaScript STARS array from repos"""
    stars = []
    for i, r in enumerate(repos, 1):
        name = r["full_name"]
        stars_count = r["stargazers_count"]
        desc = (r.get("description") or "")[:80]
        tags = []
        if r.get("language"):
            tags.append(r["language"])
        topics = r.get("topics", [])[:2]
        tags.extend(topics)
        tags = tags[:3]
        
        stars.append({
            "rank": i,
            "name": name,
            "stars": f"+{stars_count:,}/周",
            "desc": desc,
            "tags": tags,
            "url": r["html_url"]
        })
    
    return stars

def update_html(stars_data):
    """Update the STARS array in index.html"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(script_dir, "..", "index.html")
    
    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found")
        return False
    
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Build new STARS JS
    stars_js = "const STARS = [\n"
    for s in stars_data:
        tags_str = ",".join(f'"{t}"' for t in s["tags"])
        stars_js += (
            "  {"
            f"rank:{s['rank']},"
            f"name:{json.dumps(s['name'], ensure_ascii=False)},"
            f"stars:{json.dumps(s['stars'], ensure_ascii=False)},"
            f"desc:{json.dumps(s['desc'], ensure_ascii=False)},"
            f"tags:{json.dumps(s['tags'], ensure_ascii=False)},"
            f"url:{json.dumps(s['url'], ensure_ascii=False)}"
            "},\n"
        )
    stars_js += "];"
    
    # Replace old STARS
    pattern = r'const STARS = \[.*?\];'
    new_html = re.sub(pattern, stars_js, html, flags=re.DOTALL)
    
    if new_html == html:
        print("Warning: Could not find STARS array to replace")
        return False
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    
    print(f"Updated {len(stars_data)} star projects")
    return True

def main():
    print(f"CodeCraft Star Update - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    repos = fetch_weekly_stars()
    if not repos:
        print("No repos found, exiting")
        sys.exit(1)
    
    print(f"Found {len(repos)} trending repos:")
    for r in repos:
        print(f"  ⭐ {r['stargazers_count']:>6} {r['full_name']}")
    
    stars_data = generate_stars_js(repos)
    
    # Output as JSON for manual update
    print("\n=== STARS JSON ===")
    print(json.dumps(stars_data, ensure_ascii=False, indent=2))
    
    # Try to auto-update HTML
    if update_html(stars_data):
        print("\n[ok] HTML updated successfully")
    else:
        print("\n[warning] Manual update needed - copy the JSON above")

if __name__ == "__main__":
    main()
