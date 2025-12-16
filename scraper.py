from playwright.sync_api import sync_playwright
import json

URL = "https://www.sofascore.com/football"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, timeout=60000)

    # استنى تحميل المباريات
    page.wait_for_selector('[data-testid="event-list"]', timeout=60000)

    matches = []

    events = page.query_selector_all('[data-testid="event-list-item"]')

    for e in events:
        try:
            home = e.query_selector('[data-testid="home-team-name"]').inner_text()
            away = e.query_selector('[data-testid="away-team-name"]').inner_text()
            score = e.query_selector('[data-testid="event-score"]').inner_text()
            status = e.query_selector('[data-testid="event-status"]').inner_text()

            matches.append({
                "home": home.strip(),
                "away": away.strip(),
                "score": score.strip(),
                "status": status.strip()
            })
        except:
            continue

    browser.close()

print("MATCHES FOUND:", len(matches))

with open("matches_today.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, ensure_ascii=False, indent=2)
