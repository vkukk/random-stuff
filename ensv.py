#!/usr/bin/env python3
import urllib.request
import json
import time
import subprocess
import sys
from pathlib import Path

ROOT_ID = 3905
BASE_API = "https://services.err.ee/api/v2/vodContent/getContentPageData"
BASE_URL = "https://jupiter.err.ee"

SEASONS = {
     1: 1609149368,  2: 1015865,      3: 1017876,      4: 1022140,
     5: 1024801,     6: 1032343,      7: 1608333248,   8: 1608227200,
     9: 1608242526, 10: 1608264978,  11: 1608271326,  12: 1608286953,
    13: 1054787,    14: 1608106480,  15: 1608457790,  16: 1609068245,
}

def fetch_episodes(season_num, first_content_id):
    url = f"{BASE_API}?contentId={first_content_id}&rootId={ROOT_ID}&page=web"
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
    season_list = data["data"]["seasonList"]["items"]
    for season in season_list:
        if season["id"] == season_num and "contents" in season:
            return sorted(season["contents"], key=lambda x: x["episode"])
    return []

def main():
    output_dir = Path("ensv")
    output_dir.mkdir(exist_ok=True)

    seasons_to_get = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else sorted(SEASONS)

    for season_num in seasons_to_get:
        print(f"\n=== Season {season_num} ===")
        episodes = fetch_episodes(season_num, SEASONS[season_num])

        if not episodes:
            print(f"  No episodes found, skipping.")
            continue

        for ep in episodes:
            ep_id = ep["id"]
            ep_num = ep["episode"]
            url = f"{BASE_URL}/{ep_id}/ensv"
            out_template = str(output_dir / f"S{season_num:02d}E{ep_num:03d}.%(ext)s")

            print(f"  S{season_num:02d}E{ep_num:03d} ({ep_id})")
            subprocess.run([
            "yt-dlp",
            "-f", "bestvideo+bestaudio[language=et]/bestvideo+bestaudio",
            "--merge-output-format", "mp4",
            "-o", out_template,
            url
        ])
            time.sleep(1)

if __name__ == "__main__":
    main()
