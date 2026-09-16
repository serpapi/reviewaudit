"""sincere: is this rating real? Given a Google Maps place, read its reviews for the tells of manipulation."""

import argparse
import os
import re
import unicodedata
from pathlib import Path

import json
from collections import Counter

from . import norms, signals
from .api import Api
from .report import docket, render


def locality(place):
    """The district-and-city part of the address, postcodes dropped: 'Beşiktaş/İstanbul', 'London', 'Dubai'."""
    parts = [p for p in re.split(r",| - ", place.get("address", "")) if p.strip()]
    return " ".join(t for t in re.split(r"\s+", parts[-2].strip()) if not re.search(r"\d", t)) if len(parts) >= 2 else ""


def slug(place):
    """Title plus locality, so two branches of one chain get two files: nusr-et-steakhouse-besiktas-istanbul."""
    ascii = lambda t: unicodedata.normalize("NFKD", t.lower().replace("ı", "i")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii(f"{place['title']} {locality(place)}")).strip("-")


def main():
    ap = argparse.ArgumentParser(prog="sincere", description=__doc__)
    ap.add_argument("place", nargs="?", help="a Maps search ('Nusr-Et Steakhouse Etiler') or a data_id (0x…:0x…)")
    ap.add_argument("--reviews", type=int, default=200, help="newest reviews to read (default 200 ≈ 10 calls)")
    ap.add_argument("--lookups", type=int, default=30, help="reviewer histories to pull (1 call each)")
    ap.add_argument("--hl", default="en")
    ap.add_argument("--out", help="report path (default reports/<place>.html)")
    ap.add_argument("--layout", default="report", choices=["report", "brief", "grid"], help="page shape (default report: the case file)")
    ap.add_argument("--norms", action="store_true", help="rebuild norms.json and the docket (reports/sincere.html) from every case under reports/, then exit")
    args = ap.parse_args()
    if args.norms:
        n = norms.build("reports")
        Path("reports/sincere.html").write_text(docket("reports"))
        print(f"norms from {n['places']} places: " + ", ".join(f"{k} {v['median']:.2f}" for k, v in n["measures"].items()) + " → reports/sincere.html")
        return

    key = os.environ.get("SERPAPI_KEY") or os.environ.get("SERPAPI_API_KEY")
    if not key:
        raise SystemExit("set SERPAPI_KEY")
    api = Api(key, hl=args.hl)

    place = api.place(args.place)
    raw = api.reviews(place["data_id"], args.reviews)
    place = {**api.place_info, **{k: v for k, v in place.items() if v}}  # search hit fills what place_info lacks
    reviews = [x for x in map(signals.parse, raw) if x]
    third_party = Counter(r.get("source", "?") for r in raw if r["user"].get("contributor_id") is None)
    print(f"{place['title']} · {place.get('rating')}★ from {place.get('reviews')} reviews · read {len(reviews)} newest"
          + (f" · left out {sum(third_party.values())} from {', '.join(third_party)}" if third_party else ""))

    # cheap tells first, so the paid lookups go to the reviewers they point at
    signals.account_tells(reviews)
    signals.burst_tells(reviews)
    signals.echo_tells(reviews)
    signals.staff_names(reviews, place["title"], place.get("address", ""))
    signals.close_pairs(reviews)
    todo = signals.lookup_candidates(reviews, args.lookups)
    histories = {r.user_id: api.contributor(r.user_id) for r in todo}
    print(f"looked up {len(histories)} reviewer histories")

    result = signals.analyze(reviews, histories, place["data_id"], place["title"], place.get("address", ""))
    v = result["verdict"]
    print(f"{v['tier']} · {v['padded']:.0%} of five-star reviews suspect · sample {result['sample_rating']} → {result['clean_rating']} without them")
    for t, n in result["tell_counts"].most_common():
        print(f"  {n:3d}  {t}")

    out = Path(args.out or f"reports/{slug(place)}{'' if args.layout == 'report' else '-' + args.layout}.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(place, reviews, result, api, third_party, args.layout))
    out.with_suffix(".json").write_text(json.dumps(dict(
        title=place["title"], where=locality(place), data_id=place["data_id"], rating=place.get("rating"), reviews=place.get("reviews"), read=len(reviews),
        tier=v["tier"], padded=round(v["padded"], 3), sample_rating=result["sample_rating"], clean_rating=result["clean_rating"],
        taken_out=len(result["suspects"]), measures=result["measures"], report=out.name,
    ), ensure_ascii=False, indent=1))
    print(f"→ {out}  ({api.calls} calls, {api.cached} from cache)")
