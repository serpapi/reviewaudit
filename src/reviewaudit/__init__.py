"""reviewaudit: is this rating real? Given a Google Maps place, read its reviews for the tells of manipulation."""

import argparse
from importlib.metadata import version
from . import norms
from .core import NoKey, read_place
from .paths import REPORTS
from .report import docket


def main():
    ap = argparse.ArgumentParser(prog="reviewaudit", description=__doc__)
    ap.add_argument("place", nargs="?", help="a Maps search ('Nusr-Et Steakhouse Etiler'), a data_id (0x…:0x…), or `serve`")
    ap.add_argument("--reviews", type=int, default=200, help="newest reviews to read (default 200 ≈ 10 calls)")
    ap.add_argument("--lookups", type=int, default=30, help="reviewer histories to pull (1 call each)")
    ap.add_argument("--hl", default="en")
    ap.add_argument("--port", type=int, default=8811, help="port for `reviewaudit serve`")
    ap.add_argument("--no-open", action="store_true", help="don't open the browser on `reviewaudit serve`")
    ap.add_argument("--reload", action="store_true", help="restart the server when the code changes (for development)")
    ap.add_argument("--version", action="version", version=f"reviewaudit {version('reviewaudit')}")
    ap.add_argument("--norms", action="store_true", help="rebuild norms.json and the docket (reports/reviewaudit.html) from every case under reports/, then exit")
    args = ap.parse_args()

    if args.norms:
        n = norms.build(REPORTS)
        (REPORTS / "reviewaudit.html").write_text(docket(REPORTS))
        print(f"norms from {n['places']} places: " + ", ".join(f"{k} {v['median']:.2f}" for k, v in n["measures"].items()) + f" → {REPORTS}/reviewaudit.html")
        return
    if args.place == "serve":
        from .web import serve

        return serve(args.port, open_browser=not args.no_open, reload=args.reload)
    if not args.place:
        ap.error("give a place, or `serve`")

    def say(stage, done, total, note, **_):
        if note:
            print(f"{stage:9} {done:>3}/{total:<3} {note}")

    try:
        s = read_place(args.place, reviews=args.reviews, lookups=args.lookups, hl=args.hl, progress=say)
    except NoKey as e:
        raise SystemExit(str(e))
    print(f"→ {REPORTS / s['report']}  ({s['calls']} calls, {s['cached']} from cache)")
