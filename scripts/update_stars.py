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
from datetime import datetime

def fetch_trending(language="", since="weekly"):
    """Fetch trending repos from GitHub unofficial API"""
    url = f"https://api.github.com/search/repositories?q=stars:>100+pushed:>2025-01-01&sort=stars&order=desc&per_page=10"
    if language:
        url += f"+language:{language}"
    
    req = urllib.request.Request(url, headers={
        "User-Agent": "CodeCraft/1.0",
        "Accept": "application/vnd.github.v3+json"
    })
    
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        return data.get("items", [])
    except Exception as e:
        print(f"Error fetching trending: {e}")
        return []

def fetch_weekly_stars():
    """Get repos with most stars gained this week"""
    # Use GitHub search API to find recently created popular repos
    queries = [
        "stars:>500+created:>2025-06-01+language:javascript",
        "stars:>500+created:>2025-06-01+language:python",
        "stars:>500+created:>2025-06-01+language:typescript",
    ]
    
    all_repos = []
    for q in queries:
        url = f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=3"
        req = urllib.request.Request(url, headers={
            "User-Agent": "CodeCraft/1.0",
            "Accept": "application/vnd.github.v3+json"
        })
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read())
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
        stars_js += '  {rank:' + str(s["rank"]) + ',name:"' + s["name"] + '","stars":"' + s["stars"] + '","desc":"' + s["desc"] + '","tags":[' + tags_str + '],url:"' + s["url"] + '"},\n'
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
        print("\n✅ HTML updated successfully")
    else:
        print("\n⚠️  Manual update needed - copy the JSON above")

if __name__ == "__main__":
    main()
