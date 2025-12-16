import requests
from datetime import datetime, timedelta
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Referer": "https://www.fotmob.com/"
}

def fetch_day(day):
    date_str = day.strftime("%Y-%m-%d")
    url = f"https://www.fotmob.com/api/matches?date={date_str}&timezone=UTC"

    res = requests.get(url, headers=HEADERS, timeout=20)
    if res.status_code != 200:
        return []

    try:
        data = res.json()
    except:
        return []

    matches = []
    for league in data.get("leagues", []):
        for m in league.get("matches", []):
            matches.append({
                "id": m.get("id"),
                "league": league.get("name"),
                "home": m.get("home", {}).get("name"),
                "away": m.get("away", {}).get("name"),
                "homeScore": m.get("home", {}).get("score"),
                "awayScore": m.get("away", {}).get("score"),
                "status": m.get("status", {}).get("reason", {}).get("short"),
                "utcTime": m.get("status", {}).get("utcTime")
            })
    return matches


if __name__ == "__main__":
    today = datetime.utcnow().date()

    all_matches = []
    for offset in [-1, 0, 1]:  # أمس / اليوم / بكرة
        all_matches.extend(fetch_day(today + timedelta(days=offset)))

    # إزالة التكرار
    unique = {m["id"]: m for m in all_matches if m.get("id")}
    matches = list(unique.values())

    print("MATCHES FOUND:", len(matches))

    with open("matches_today.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
