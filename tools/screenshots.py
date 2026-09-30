"""The README images, taken against a running app so they are never hand-cropped.

    uv run python tools/demo.py &          # an invented Google Maps: no real place or reviewer in the images
    uv run python tools/screenshots.py [http://localhost:8811]

Every shot is clipped to real element boundaries, so nothing is ever cut through the middle
of a card. Edit CASE / INSIGHTS / SEARCH / RUN below to change which places appear.
"""

import sys
import time
import urllib.parse
import urllib.request

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8811"
ONLY = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None  # e.g. home,cases
OUT = "docs"
CASE = "harbor-lights-dinner-cruise-port-arden.html"  # the hero: the clearest case of bought reviews
INSIGHTS = "anchor-street-deli-port-arden.html"  # a place with enough unhappy reviews to have complaints
SEARCH = "/search?q=pizza&near=Port%20Arden"
RUN = "Driftwood Pizza Co."  # somewhere not yet read, so the run has work to do
WIDTH, SCALE = 1280, 2


def settle(page, ms=2600):
    page.evaluate("document.documentElement.dataset.theme = 'light'; document.activeElement && document.activeElement.blur()")
    page.wait_for_load_state("networkidle")
    page.evaluate("""() => new Promise(done => {
        const pending = [...document.images].filter(i => !i.complete);
        if (!pending.length) return done();
        let left = pending.length;
        const tick = () => (--left <= 0) && done();
        pending.forEach(i => { i.addEventListener('load', tick); i.addEventListener('error', tick); });
        setTimeout(done, 6000);
    })""")
    time.sleep(ms / 1000)


def shot(page, path, *, through=None, height=None):
    """Clip from the top of the page down to the bottom of `through` (a selector), or a height."""
    if through:
        box = page.locator(through).last.bounding_box()
        height = box["y"] + box["height"] + 8
    page.screenshot(path=f"{OUT}/{path}", full_page=True, clip={"x": 0, "y": 0, "width": WIDTH, "height": round(height)})


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_context(viewport={"width": WIDTH, "height": 900}, device_scale_factor=SCALE, color_scheme="light").new_page()

    def want(name):
        return not ONLY or name in ONLY

    # the hero: the place card and the verdict, down to the end of the timeline
    if want("report"):
        page.goto(f"{BASE}/{CASE}")
        settle(page, 3200)
        shot(page, "report.png", through="#when")

    # the insights band, as its own block
    if want("insights"):
        page.goto(f"{BASE}/{INSIGHTS}")
        settle(page, 3000)
        page.locator("h2.band ~ .grid").first.screenshot(path=f"{OUT}/insights.png")

    # home, down to the end of the case cards
    if want("home"):
        page.goto(f"{BASE}/")
        settle(page)
        shot(page, "home.png", through=".cards a.case")

    # search results, whole rows only
    if want("search"):
        page.goto(f"{BASE}{SEARCH}")
        settle(page)
        shot(page, "search.png", through=".hits li:nth-child(6)")

    # the cases list, whole rows only
    if want("cases"):
        page.goto(f"{BASE}/cases")
        settle(page)
        shot(page, "cases.png", through="table.docket tr:nth-child(9)")

    # a run, caught while it pulls records
    if want("run"):
      req = urllib.request.Request(f"{BASE}/runs", data=urllib.parse.urlencode(dict(q=RUN, title=RUN)).encode(), method="POST")
      req.add_header("Content-Type", "application/x-www-form-urlencoded")
      page.goto(urllib.request.urlopen(req).geturl())
      page.evaluate("document.documentElement.dataset.theme = 'light'")
      for _ in range(150):
          time.sleep(1)
          count = page.evaluate("(document.querySelector('.steps li.now[data-stage=records] .count') || {}).textContent || ''")
          if count and int(count.split("/")[0]) >= 9:
              break
      shot(page, "run.png", through=".log li:nth-child(8)")
    browser.close()

print(f"{OUT}/" + "{report,insights,home,search,cases,run}.png")
