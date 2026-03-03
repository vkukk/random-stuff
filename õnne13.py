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

# All 33 seasons with their first episode content IDs (from the API)
SEASONS = {
    1: 1608211729, 2: 1608236037, 3: 1608236076, 4: 1608236154,
    5: 1608236157, 6: 1608235980, 7: 894488,     8: 894997,
    9: 895661,    10: 903607,    11: 917521,    12: 933396,
    13: 949618,   14: 964507,    15: 977142,    16: 997936,
    17: 1019627,  18: 1054829,   19: 1075087,   20: 1098091,
    21: 1113580,  22: 1130672,   23: 1152666,   24: 1217944,
    25: 894461,   26: 1089733,   27: 1128044,   28: 1608195853,
    29: 1608572437, 30: 1608954215, 31: 1609324418,
    32: 1609675298, 33: 1609939942
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
    output_dir = Path("õnne13")
    output_dir.mkdir(exist_ok=True)

    # Optionally filter seasons via CLI args: python script.py 1 2 3
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
            url = f"{BASE_URL}/{ep_id}/onne-13"
            out_template = str(output_dir / f"S{season_num:02d}E{ep_num:03d}.%(ext)s")

            print(f"  S{season_num:02d}E{ep_num:03d} ({ep_id})")
            subprocess.run([
                "yt-dlp",
                "--merge-output-format", "mp4",
                "-o", out_template,
                url
            ])
            time.sleep(1)  # be polite

if __name__ == "__main__":
    main()
