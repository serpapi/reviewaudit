"""Reproducible README screenshots: a fixed 1280px viewport at 2x, light theme, against a running app.

    uv run reviewaudit serve --no-open &
    uv run python tools/screenshots.py [http://localhost:8811] [a place to start a run on]
"""

import sys
import time
import urllib.parse
import urllib.request

from playwright.sync_api import sync_playwright

base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8811"
run_query = sys.argv[2] if len(sys.argv) > 2 else "Pizza & Passione Napoli"
out = "docs"


def settle(page, ms=2500):
    page.evaluate("document.documentElement.dataset.theme = 'light'")
    page.wait_for_load_state("networkidle")
    time.sleep(ms / 1000)


with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1280, "height": 860}, device_scale_factor=2, color_scheme="light")
    page = ctx.new_page()

    page.goto(f"{base}/")
    settle(page)
    page.screenshot(path=f"{out}/home.png", full_page=True)

    page.goto(f"{base}/search?q=pizza&near=Naples,%20Italy")
    settle(page)
    page.screenshot(path=f"{out}/search.png", full_page=True, clip={"x": 0, "y": 0, "width": 1280, "height": 960})

    page.goto(f"{base}/cases")
    settle(page)
    page.screenshot(path=f"{out}/cases.png", full_page=True, clip={"x": 0, "y": 0, "width": 1280, "height": 900})

    # a run, caught while it pulls records
    req = urllib.request.Request(f"{base}/runs", data=urllib.parse.urlencode(dict(q=run_query, title=run_query)).encode(), method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    run_url = urllib.request.urlopen(req).geturl()
    page.goto(run_url)
    page.evaluate("document.documentElement.dataset.theme = 'light'")
    for _ in range(120):
        time.sleep(1)
        count = page.evaluate("(document.querySelector('.steps li.now[data-stage=records] .count') || {}).textContent || ''")
        if count and int(count.split("/")[0]) >= 8:
            break
    page.screenshot(path=f"{out}/run.png", full_page=True, clip={"x": 0, "y": 0, "width": 1280, "height": 760})

    # the richest case as the hero
    page.goto(f"{base}/nusr-et-steakhouse-besiktas-istanbul.html")
    settle(page, 3500)
    page.screenshot(path=f"{out}/report.png", full_page=True, clip={"x": 0, "y": 0, "width": 1280, "height": 1280})
    browser.close()
print("docs/{home,search,cases,run,report}.png")
