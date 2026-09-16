"""What is typical. Every case writes its measures next to its report; `sincere --norms` folds them into norms.json,
and the report then shows each number beside the median and the middle 80% of every place read so far."""

import json
from pathlib import Path
from statistics import median

NORMS = Path(__file__).parent / "norms.json"
LABELS = {
    "first_share": ("reviewers with no record", "share of reviews from accounts reviewing for the first time"),
    "first_gap": ("first-timer five-star gap", "how much more often first-timers give five stars than accounts with 4 to 50 reviews"),
    "close_ratio": ("batches", "five-star pairs minutes apart, as a multiple of what the hours people post at predict"),
    "staff_share": ("reviews naming staff", "share of reviews that name a waiter, doctor or guide"),
    "photo_share": ("five-stars with a photo", "share of five-star reviews that carry a photo"),
    "text_share": ("five-stars with text", "share of five-star reviews that say anything"),
    "five_share": ("five-star share", "share of the reviews read that are five stars"),
}


def load():
    try:
        return json.loads(NORMS.read_text())
    except FileNotFoundError:
        return None


def build(reports_dir):
    rows = [json.loads(p.read_text()) for p in Path(reports_dir).glob("*.json")]
    out = {"places": len(rows), "measures": {}}
    for key in LABELS:
        vals = sorted(r["measures"][key] for r in rows if r.get("measures", {}).get(key) is not None)
        if len(vals) >= 5:
            out["measures"][key] = dict(median=median(vals), p10=vals[len(vals) // 10], p90=vals[-max(1, len(vals) // 10)], n=len(vals))
    NORMS.write_text(json.dumps(out, indent=1))
    return out
