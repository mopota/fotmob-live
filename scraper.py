import requests
from datetime import datetime, timedelta
import json
import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Referer": "https://www.fotmob.com/"
}

def fetch_by_date(d):
    # صيغة بتشتغل بثبات مع FotMob
    date_str = d.strftime("%Y%m%d")
    url = f"https://www.fotmob.com/api/matches?date={date_str}"
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
                "score": f'{m.get("home", {}).get("score", 0)}-{m.get("away", {}).get("awayScore", m.get("away", {}).get("score", 0))}',
                "status": m.get("status", {}).get("reason", {}).get("short", "")
            })
    return matches

if __name__ == "__main__":
    today_utc = datetime.utcnow().date()

    all_matches = []
    # أمس + اليوم + بكرة (عشان فرق التوقيت)
    for delta in [-1, 0, 1]:
        all_matches.extend(fetch_by_date(today_utc + timedelta(days=delta)))

    # إزالة التكرار
    uniq = {m["id"]: m for m in all_matches if m.get("id")}
    matches = list(uniq.values())

    print("MATCHES FOUND:", len(matches))

    with open("matches_today.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)

    sys.exit(0)
