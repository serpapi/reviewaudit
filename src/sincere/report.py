"""One self-contained HTML page per place. Charts are inline SVG laid out here; the template only draws."""

from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .signals import TELLS, TRUST, bursts as _bursts  # noqa: F401  (TELLS/TRUST feed the method table)

env = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"), autoescape=True)
env.filters["thousands"] = lambda n: f"{n:,}" if isinstance(n, (int, float)) else n
env.filters["pct"] = lambda x: f"{x:.0%}" if x is not None else "–"
env.filters["day"] = lambda d: d.strftime("%-d %b %Y")


def timeline(reviews, suspects, windows, width=880, height=300, r=4):
    """Every review as a dot: x = when, y = stars, swarmed so a busy week reads as a busy week. The axis starts at
    the 10th-percentile date so a handful of edited-years-ago reviews (which 'newest first' still returns) don't
    flatten the last two months into a sliver."""
    dates = sorted(x.date for x in reviews)
    lo, hi = dates[len(dates) // 10], dates[-1]
    span = max((hi - lo).total_seconds(), 86400)
    left, right, top, bottom = 56, 16, 34, 36
    plot_w, plot_h = width - left - right, height - top - bottom
    row_h = plot_h / 5
    suspect_ids = {x.id for x in suspects}
    pts, earlier, placed = [], [], {s: [] for s in range(1, 6)}
    for x in sorted(reviews, key=lambda x: x.date):
        entry = dict(rating=x.rating, suspect=x.id in suspect_ids, name=x.user_name, date=x.date.strftime("%-d %b %Y"), tells=", ".join(x.tells), link=x.link, score=x.score)
        if x.date < lo:
            earlier.append(entry)
            continue
        cx = left + (x.date - lo).total_seconds() / span * plot_w
        cy = top + (5 - x.rating) * row_h + row_h / 2
        gap = 2 * r + 1
        for k in range(0, 40):  # 0, -1, +1, -2, +2 ... slots off the row centre, first free one wins
            dy = (k + 1) // 2 * gap * (1 if k % 2 else -1)
            if abs(dy) > row_h / 2 - r:
                dy = 0
                break
            if all((cx - px) ** 2 + (dy - py) ** 2 >= gap * gap for px, py in placed[x.rating]):
                break
        placed[x.rating].append((cx, dy))
        entry.update(x=round(cx, 1), y=round(cy + dy, 1))
        pts.append(entry)
    ticks, d = [], datetime(lo.year, lo.month, 1, tzinfo=timezone.utc)
    step_months = 1 if span < 400 * 86400 else 3 if span < 1200 * 86400 else 12
    while d <= hi:
        if d >= lo:
            ticks.append(dict(x=round(left + (d - lo).total_seconds() / span * plot_w, 1), label=d.strftime("%b %Y" if d.month == 1 or step_months > 1 or not ticks else "%b")))
        m = d.month - 1 + step_months
        d = d.replace(year=d.year + m // 12, month=m % 12 + 1)
    bands = []
    for name, ws in windows.items():
        for w in ws:
            if w["end"] >= lo:
                x0 = left + max(0, (w["start"] - lo).total_seconds()) / span * plot_w
                x1 = left + (w["end"] - lo).total_seconds() / span * plot_w
                bands.append(dict(x=round(x0 - r - 2, 1), w=round(max(x1 - x0 + 2 * r + 4, 8), 1), label=f"{w['n']} {'five' if name == 'praise burst' else 'one'}-star in {(w['end'] - w['start']).days + 1} days, {w['expected']:g} expected", attack=name == "attack burst"))
    rows = [dict(y=round(top + (5 - s) * row_h + row_h / 2, 1), label=s) for s in range(5, 0, -1)]
    return dict(width=width, height=height, left=left, right=right, top=top, bottom=bottom, plot_w=plot_w, plot_h=plot_h, points=pts, earlier=earlier, ticks=ticks, bands=bands, rows=rows, lo=lo, hi=hi, r=r)


def stars_table(reviews, suspects):
    ids = {r.id for r in suspects}
    total = len(reviews)
    return [dict(stars=s, n=sum(r.rating == s for r in reviews), sus=sum(r.rating == s and r.id in ids for r in reviews), share=sum(r.rating == s for r in reviews) / total) for s in range(5, 0, -1)]


def sentence(place, reviews, result):
    v, fives = result["verdict"], [r for r in reviews if r.rating == 5]
    k = sum(r.rating == 5 for r in result["suspects"])
    d = result["depth"]
    parts = []
    if k:
        parts.append(f"{k} of the {len(fives)} recent five-star reviews are more than this place's own reviewers explain.")
    else:
        parts.append(f"Nothing in the last {len(reviews)} reviews goes beyond what this place's own reviewers explain.")
    if result["base_share"] is not None and d[0]["share"] is not None and d[0]["n"] >= 5:
        base, first = result["base_share"], d[0]["share"]
        if first - base >= 0.08:
            parts.append(f"Accounts with a record give it five stars {base:.0%} of the time; accounts reviewing for the first time, {first:.0%}.")
        else:
            parts.append(f"First-time reviewers and accounts with a record give it five stars at the same rate ({first:.0%} and {base:.0%}).")
    deep = d[-1]
    if result["base_share"] is not None and deep["n"] >= 10 and result["base_share"] - deep["share"] >= 0.15:
        parts.append(f"Its most seasoned reviewers, with 51 or more reviews, give it five stars {deep['share']:.0%} of the time.")
    for w in result["bursts"].get("praise burst", []):
        parts.append(f"{w['n']} five-stars landed between {w['start']:%-d %b} and {w['end']:%-d %b} when {w['expected']:g} would be normal.")
    for w in result["bursts"].get("attack burst", []):
        parts.append(f"{w['n']} one-stars landed between {w['start']:%-d %b} and {w['end']:%-d %b} when {w['expected']:g} would be normal.")
    if result["echoes"]:
        n = sum(len(c) for c in result["echoes"])
        parts.append(f"{n} reviews repeat each other's wording.")
    if any("ring" in r.tells for r in reviews):
        parts.append("A group of reviewers keeps turning up at the same other places.")
    return " ".join(parts)


def render(place, reviews, result, api):
    tpl = env.get_template("report.html")
    dates = sorted(r.date for r in reviews)
    checked = [r for r in reviews if r.history]
    return tpl.render(
        place=place,
        reviews=reviews,
        result=result,
        sentence=sentence(place, reviews, result),
        tl=timeline(reviews, result["suspects"], result["bursts"]),
        stars=stars_table(reviews, result["suspects"]),
        checked=checked,
        first=dates[0],
        last=dates[-1],
        tells=TELLS,
        trust=TRUST,
        calls=api.calls + api.cached,
        generated=datetime.now().strftime("%-d %B %Y"),
    )
