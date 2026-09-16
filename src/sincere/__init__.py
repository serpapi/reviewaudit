"""sincere: is this rating real? Given a Google Maps place, read its reviews for the tells of manipulation."""

import argparse
import os
import re
import unicodedata
from pathlib import Path

from . import signals
from .api import Api
from .report import render


def main():
    ap = argparse.ArgumentParser(prog="sincere", description=__doc__)
    ap.add_argument("place", help="a Maps search ('Nusr-Et Steakhouse Etiler') or a data_id (0x…:0x…)")
    ap.add_argument("--reviews", type=int, default=200, help="newest reviews to read (default 200 ≈ 10 calls)")
    ap.add_argument("--lookups", type=int, default=30, help="reviewer histories to pull (1 call each)")
    ap.add_argument("--hl", default="en")
    ap.add_argument("--out", help="report path (default reports/<place>.html)")
    args = ap.parse_args()

    key = os.environ.get("SERPAPI_KEY") or os.environ.get("SERPAPI_API_KEY")
    if not key:
        raise SystemExit("set SERPAPI_KEY")
    api = Api(key, hl=args.hl)

    place = api.place(args.place)
    raw = api.reviews(place["data_id"], args.reviews)
    place = {**api.place_info, **{k: v for k, v in place.items() if v}}  # search hit fills what place_info lacks
    reviews = [signals.parse(r) for r in raw]
    print(f"{place['title']} · {place.get('rating')}★ from {place.get('reviews')} reviews · read {len(reviews)} newest")

    # cheap tells first, so the paid lookups go to the reviewers they point at
    signals.account_tells(reviews)
    signals.burst_tells(reviews)
    signals.echo_tells(reviews)
    todo = signals.lookup_candidates(reviews, args.lookups)
    histories = {r.user_id: api.contributor(r.user_id) for r in todo}
    print(f"looked up {len(histories)} reviewer histories")

    result = signals.analyze(reviews, histories, place["data_id"], place["title"])
    v = result["verdict"]
    print(f"{v['tier']} · {v['padded']:.0%} of five-star reviews suspect · sample {result['sample_rating']} → {result['clean_rating']} without them")
    for t, n in result["tell_counts"].most_common():
        print(f"  {n:3d}  {t}")

    slug = unicodedata.normalize("NFKD", place["title"].lower().replace("ı", "i")).encode("ascii", "ignore").decode()
    out = Path(args.out or f"reports/{re.sub(r'[^a-z0-9]+', '-', slug).strip('-')}.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(place, reviews, result, api))
    print(f"→ {out}  ({api.calls} calls, {api.cached} from cache)")
