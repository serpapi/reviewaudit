"""Find candidate places to audit, cheaply, before spending 42 credits on a full read.

    uv run python tools/prospect.py "moving company" "Los Angeles, California" ...

One credit per search, one per candidate looked at in detail. It ranks by the shape that
bought reviews leave behind: a high rating carried by a wall of five stars, with a fat
one-star tail underneath from the customers who actually turned up.
"""

import sys

from reviewaudit.core import api_from_env

api = api_from_env()
pairs = list(zip(sys.argv[1::2], sys.argv[2::2]))
seen, rows = set(), []

for query, near in pairs:
    data = api.search(engine="google_maps", q=query, location=near, z=12)
    for hit in data.get("local_results", []) or [data.get("place_results")]:
        if not hit or hit.get("data_id") in seen:
            continue
        seen.add(hit["data_id"])
        if (hit.get("rating") or 0) < 4.4 or (hit.get("reviews") or 0) < 120:
            continue  # a low rating has nothing to hide; too few reviews and the tail says nothing
        place = api.search(engine="google_maps", q=f"{hit['title']} {hit.get('address', '')}").get("place_results") or {}
        summary = {r["stars"]: r["amount"] for r in place.get("rating_summary") or []}
        total = sum(summary.values())
        if total < 120:
            continue
        one, four = summary.get(1, 0) / total, summary.get(4, 0) / total
        five = summary.get(5, 0) / total
        if four > 0.025 or five < 0.88 or one < 0.03:
            continue  # what is wanted is the missing middle: a wall of fives, no four-star tail, and angry customers underneath
        rows.append(dict(score=one * five / (four + 0.004), one=one, four=four, five=five,
                         rating=hit["rating"], n=total, title=hit["title"], where=hit.get("address", "")[-28:], data_id=hit["data_id"], q=query))

rows.sort(key=lambda r: -r["score"])
print(f"{'rating':>6} {'reviews':>8} {'5★':>5} {'4★':>5} {'1★':>5}  place")
for r in rows[:20]:
    print(f"{r['rating']:>6} {r['n']:>8} {r['five']:>5.0%} {r['four']:>5.0%} {r['one']:>5.0%}  {r['title'][:38]:38} {r['where']}  {r['data_id']}")
print(f"\n{api.calls} credits spent, {api.cached} from cache")
