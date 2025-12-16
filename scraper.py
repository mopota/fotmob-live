import requests
from datetime import date
import json

def get_today_matches():
    today = date.today().strftime("%Y-%m-%d")
    url = f"https://www.fotmob.com/api/matches?date={today}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "Referer": "https://www.fotmob.com/"
    }

    res = requests.get(url, headers=headers, timeout=20)
    data = res.json()

    matches = []

    for league in data.get("leagues", []):
        for m in league.get("matches", []):
            matches.append({
                "id": m["id"],
                "league": league["name"],
                "home": m["home"]["name"],
                "away": m["away"]["name"],
                "score": f'{m["home"]["score"]}-{m["away"]["score"]}',
                "status": m.get("status", {}).get("reason", {}).get("short", "")
            })

    return matches


if __name__ == "__main__":
    matches = get_today_matches()

    with open("matches_today.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
