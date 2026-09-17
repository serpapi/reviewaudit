"""One place, end to end: find it, read its reviews, pull the records worth pulling, analyse, write the case."""

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

from . import signals
from .api import Api
from .paths import REPORTS, api_key
from .report import render


def locality(place):
    """The district-and-city part of the address, postcodes dropped: 'Beşiktaş/İstanbul', 'London', 'Dubai'."""
    parts = [p for p in re.split(r",| - ", place.get("address", "")) if p.strip()]
    return " ".join(t for t in re.split(r"\s+", parts[-2].strip()) if not re.search(r"\d", t)) if len(parts) >= 2 else ""


def slug(place):
    """Title plus locality, so two branches of one chain get two files: nusr-et-steakhouse-besiktas-istanbul."""
    ascii = lambda t: unicodedata.normalize("NFKD", t.lower().replace("ı", "i")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii(f"{place['title']} {locality(place)}")).strip("-")


class NoKey(Exception):
    pass


def api_from_env(hl="en"):
    key = api_key()
    if not key:
        raise NoKey("no SerpApi key: set SERPAPI_KEY, or paste it in the app")
    return Api(key, hl=hl)


def read_place(query, reviews=200, lookups=30, hl="en", out_dir=REPORTS, progress=None, api=None):
    """Runs the whole read. `progress(stage, done, total, note)` is called as it goes; returns the case summary dict."""
    say = progress or (lambda *a: None)
    api = api or api_from_env(hl)
    out_dir = Path(out_dir)

    say("place", 0, 1, f"looking up {query}")
    place = api.place(query)
    say("place", 1, 1, place.get("title") or place["data_id"])

    pages = -(-reviews // 20)
    raw = api.reviews(place["data_id"], reviews, progress=lambda n: say("reviews", min(n, reviews), reviews, f"{min(n, reviews)} of {reviews} reviews"))
    if "title" not in place:  # started from a data_id: fetch the Maps entry now that the reviews told us the name
        place = api.place_card(place["data_id"], api.place_info.get("title", ""), api.place_info.get("address", "")) or place
    place = {**api.place_info, **{k: v for k, v in place.items() if v}}  # search hit fills what place_info lacks
    rs = [x for x in map(signals.parse, raw) if x]
    third_party = Counter(r.get("source", "?") for r in raw if r["user"].get("contributor_id") is None)
    say("reviews", reviews, reviews, f"{len(rs)} reviews read" + (f", {sum(third_party.values())} third-party left out" if third_party else ""))

    # cheap tells first, so the paid lookups go to the reviewers they point at
    signals.account_tells(rs)
    signals.burst_tells(rs)
    signals.echo_tells(rs)
    signals.staff_names(rs, place["title"], place.get("address", ""))
    signals.close_pairs(rs)
    todo = signals.lookup_candidates(rs, lookups)
    histories = {}
    for i, r in enumerate(todo, 1):
        say("records", i - 1, len(todo), f"{r.user_name}, {r.user_reviews} review{'s' if r.user_reviews != 1 else ''}")
        histories[r.user_id] = api.contributor(r.user_id)
    say("records", len(todo), len(todo), f"{len(todo)} records read")

    say("analysis", 0, 1, "weighing the tells")
    result = signals.analyze(rs, histories, place["data_id"], place["title"], place.get("address", ""))
    v = result["verdict"]

    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{slug(place)}.html"
    out.write_text(render(place, rs, result, api, third_party))
    summary = dict(
        title=place["title"], where=locality(place), data_id=place["data_id"], rating=place.get("rating"), reviews=place.get("reviews"), read=len(rs),
        tier=v["tier"], padded=round(v["padded"], 3), sample_rating=result["sample_rating"], clean_rating=result["clean_rating"],
        taken_out=len(result["suspects"]), measures=result["measures"], report=out.name, slug=out.stem,
        thumbnail=place.get("thumbnail"), open_state=place.get("open_state"), type=place.get("type"), address=place.get("address"),
        calls=api.calls, cached=api.cached, tells={t: n for t, n in result["tell_counts"].most_common()},
    )
    out.with_suffix(".json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    say("done", 1, 1, f"{v['tier']}: {v['padded']:.0%} of five-star reviews beyond baseline")
    return summary


def cases(out_dir=REPORTS):
    """Every case on disk, most padded first."""
    rows = [json.loads(p.read_text()) for p in Path(out_dir).glob("*.json")]
    rows.sort(key=lambda c: -c["padded"])
    return rows
