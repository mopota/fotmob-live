import requests
from datetime import date
import json
import sys

def get_today_matches():
    today = date.today().strftime("%Y-%m-%d")
    url = f"https://www.fotmob.com/api/matches?date={today}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "Referer": "https://www.fotmob.com/"
    }

    try:
        res = requests.get(url, headers=headers, timeout=20)
    except Exception as e:
        print("REQUEST ERROR:", e)
        return []

    print("STATUS:", res.status_code)

    if res.status_code != 200:
        print("NON-200 RESPONSE")
        print(res.text[:200])
        return []

    content_type = res.headers.get("Content-Type", "")
    if "json" not in content_type:
        print("NOT JSON RESPONSE")
        print(res.text[:200])
        return []

    try:
        data = res.json()
    except Exception as e:
        print("JSON PARSE ERROR:", e)
        print(res.text[:200])
        return []

    matches = []

    for league in data.get("leagues", []):
        for m in league.get("matches", []):
            matches.append({
                "id": m.get("id"),
                "league": league.get("name"),
                "home": m.get("home", {}).get("name"),
                "away": m.get("away", {}).get("name"),
                "score": f'{m.get("home", {}).get("score", 0)}-{m.get("away", {}).get("score", 0)}',
                "status": m.get("status", {}).get("reason", {}).get("short", "")
            })

    return matches


if __name__ == "__main__":
    matches = get_today_matches()
    print("MATCHES FOUND:", len(matches))

    with open("matches_today.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)

    # مهم جدًا: نطلع دايمًا exit code 0
    sys.exit(0)
