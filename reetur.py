import subprocess
import sys
import time
import urllib.request
import json

API_URL = "https://services.err.ee/api/v2/vodContent/getContentPageData"
ROOT_ID = 3905
BASE_URL = "https://jupiter.err.ee"
SLUG = "reetur"

SEASONS = {
    1: 1130676,
    2: 1608708835,
    3: 1609544171,
}


def fetch_episodes(season_num, first_content_id):
    url = f"{API_URL}?contentId={first_content_id}&rootId={ROOT_ID}&page=web"
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read())
    season_list = data["data"]["seasonList"]["items"]
    for season in season_list:
        if season["id"] == season_num:
            return sorted(season["contents"], key=lambda e: e["episode"])
    return []


def download(seasons_to_get):
    for season_num in seasons_to_get:
        first_id = SEASONS[season_num]
        print(f"\n=== Season {season_num} ===")
        episodes = fetch_episodes(season_num, first_id)
        if not episodes:
            print(f"  No episodes found for season {season_num}")
            continue
        for ep in episodes:
            ep_num = ep["episode"]
            content_id = ep["id"]
            out_template = f"{SLUG}/S{season_num:02d}E{ep_num:03d}.%(ext)s"
            url = f"{BASE_URL}/{content_id}/{SLUG}"
            print(f"  S{season_num:02d}E{ep_num:03d} ({content_id})")
            subprocess.run([
                "yt-dlp",
                "-f", "bestvideo+bestaudio[language=et]/bestvideo+bestaudio",
                "--merge-output-format", "mp4",
                "-o", out_template,
                url
            ])
            time.sleep(1)


if __name__ == "__main__":
    if sys.argv[1:]:
        selected = [int(x) for x in sys.argv[1:]]
    else:
        selected = sorted(SEASONS.keys())
    download(selected)
    
