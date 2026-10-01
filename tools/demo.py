"""reviewaudit against an invented Google Maps: the README images, with no real business or reviewer in them.

    uv run python tools/demo.py [port]      # builds the demo cases in a temp home, then serves the app
    uv run python tools/screenshots.py      # in another shell

The places are invented and set in Portland, Maine, so the map, the addresses and the time zone are real while the
businesses are not: every name was searched on Google Maps around Portland and none of them is there. Reviews,
reviewers and their records are generated from a seed, with text drawn from `demo_text.py`. `FakeApi` answers the
same three engines the real `Api` calls, in the same shapes, so the read, the case pages and the app are the real code
over synthetic data. The padding in each place is written in on purpose (a first-timer surge, bursts, minute-apart
batches, a named waiter, echoes, a ring) so every tell has something to find. Photos are CC0 or CC BY, see demo/CREDITS.
"""

import hashlib
import os
import random
import re
import shutil
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

os.environ["REVIEWAUDIT_HOME"] = tempfile.mkdtemp(prefix="reviewaudit-demo-")
os.environ["SERPAPI_KEY"] = "demo"

from demo_text import CORPUS  # noqa: E402
from reviewaudit import core, norms, signals, web  # noqa: E402  (after the home is set)
from reviewaudit.api import Api  # noqa: E402
from reviewaudit.paths import REPORTS  # noqa: E402
from reviewaudit.report import docket  # noqa: E402

NOW = datetime(2026, 9, 20, 18, tzinfo=timezone.utc)
UTC_OFFSET = 5  # Portland is UTC-4 in summer; the app reads -5 off the longitude, and the hour chart has to agree with it

FIRST = """Mike Jessica Chris Sarah Matt Ashley Josh Amanda Dave Emily Ryan Megan Kevin Lauren Brian Katie Jason Rachel Tom Nicole Steve Heather
Dan Amy Jeff Kelly Mark Erin Nick Lindsay Andrew Molly Ben Allison Sam Courtney Tyler Brianna Kyle Hannah Greg Caitlin Pete Maddie Sean Abby
Luis Priya Wei Fatima Omar Ana Hyun Deepa Carlos Mei Andre Nadia""".split()
LAST = """Thibodeau Pelletier Michaud Gagnon Ouellette Cyr Dube Leblanc Smith Johnson Murphy O'Brien Sullivan Walsh Doyle Kelley Brennan Morrison
Hutchins Pike Bean Libby Chase Dunn Harmon Wentworth Coffin Hall Carter Mitchell Nguyen Patel Garcia Kim Chen Rossi Martin Brooks Foster Reed
Hughes Ward Bailey Palmer Shaw Fernald Stevens Haskell Pratt""".split()

# public places a local reviewer has usually been to, and a few farther off; reviewing a landmark says nothing about it
NEAR = {"Portland Head Light": (43.6231, -70.2079), "Eastern Promenade": (43.6686, -70.2424), "Back Cove Trail": (43.6787, -70.2580),
        "Portland Museum of Art": (43.6537, -70.2620), "Portland International Jetport": (43.6462, -70.3144), "Deering Oaks Park": (43.6586, -70.2719),
        "Bug Light Park": (43.6532, -70.2342), "Portland Observatory": (43.6654, -70.2483), "Victoria Mansion": (43.6515, -70.2607),
        "Crescent Beach State Park": (43.5625, -70.2348), "Mackworth Island": (43.6891, -70.2314), "Portland Public Library": (43.6580, -70.2595),
        "Hadlock Field": (43.6568, -70.2782), "Casco Bay Lines Ferry Terminal": (43.6564, -70.2478)}
FAR = {"Acadia National Park": (44.3563, -68.2155), "Fenway Park": (42.3465, -71.0971), "Boston Logan International Airport": (42.3632, -71.0136),
       "Old Orchard Beach Pier": (43.5151, -70.3724), "Dock Square, Kennebunkport": (43.3615, -70.4774), "Sugarloaf Mountain": (45.0318, -70.3131)}
ELSEWHERE_CITIES = [(39.95, -75.16), (33.75, -84.39), (29.76, -95.37), (41.88, -87.63), (25.76, -80.19), (36.17, -115.14), (40.71, -74.01), (32.78, -96.80)]

# spec: the place as Google Maps lists it, the honest reviewers' star mix, how far back 200 reviews reach, and what padding is written in
PLACES = [
    dict(title="Gull Rock Dinner Cruise", cat="cruise", type="Boat tour agency", address="Long Wharf, Commercial St, Portland, ME 04101", gps=(43.65520, -70.25135),
         phone="(207) 761-4382", website="https://gullrockcruises.com", open_state="Open ⋅ Closes 9 PM", price="$$$",
         description="Two-hour sunset dinner cruises past the Casco Bay islands and lighthouses, with a three-course menu and a full bar.",
         rating=4.7, total=1057, span=880, stars=(52, 16, 10, 6, 16), honest=118, tags="cruise boat dinner harbor",
         fake=dict(bursts=[(520, 34), (400, 33)], scatter=14, thin=0.85, text=0.25)),
    dict(title="Nonna Lucia Pizzeria", cat="pizza", type="Pizza restaurant", address="93 Middle St, Portland, ME 04101", gps=(43.65932, -70.25135),
         phone="(207) 774-2960", website="https://nonnaluciapizza.com", open_state="Open ⋅ Closes 10 PM", price="$$",
         rating=4.7, total=232, span=700, stars=(62, 18, 8, 5, 7), honest=150, tags="pizza italian restaurant",
         fake=dict(table=36, staff=["Marco", "Giulia"], thin=0.8, text=0.9)),
    dict(title="Back Cove Towing & Recovery", cat="towing", type="Towing service", address="1145 Riverside St, Portland, ME 04103", gps=(43.71194, -70.31150),
         phone="(207) 797-5531", website="https://backcovetowing.com", open_state="Open 24 hours",
         rating=5.0, total=286, span=900, stars=(94, 3, 1, 1, 1), honest=150, tags="towing",
         fake=dict(scatter=34, batches=10, thin=0.9, text=0.3)),
    dict(title="Brightwater Dental", cat="dental", type="Dentist", address="1601 Forest Ave, Portland, ME 04103", gps=(43.69739, -70.30756),
         phone="(207) 878-1145", website="https://brightwaterdentalme.com", open_state="Closed ⋅ Opens 8 AM Mon",
         rating=4.9, total=312, span=760, stars=(82, 8, 3, 2, 5), honest=160, tags="dentist dental",
         fake=dict(scatter=18, echo=16, ring=6, thin=0.5, text=1.0)),
    dict(title="Old Mill Steakhouse", cat="steak", type="Steak house", address="295 Fore St, Portland, ME 04101", gps=(43.65522, -70.25601),
         phone="(207) 772-8810", website="https://oldmillsteakhouseme.com", open_state="Open ⋅ Closes 10 PM", price="$$$$",
         rating=4.4, total=2140, span=120, stars=(60, 20, 8, 5, 7), honest=170, tags="steak restaurant", langs=True,
         fake=dict(scatter=30, thin=0.9, text=0.3)),
    dict(title="Keel & Key Locksmith", cat="locksmith", type="Locksmith", address="1037 Forest Ave, Portland, ME 04103", gps=(43.68299, -70.29008),
         phone="(207) 871-0472", website="https://keelandkeylocksmith.com", open_state="Open 24 hours",
         rating=4.9, total=894, span=1000, stars=(88, 6, 2, 1, 3), honest=182, tags="locksmith",
         fake=dict(scatter=8, batches=6, thin=0.9, text=0.4)),
    dict(title="Seaglass Car Wash", cat="carwash", type="Car wash", address="1280 Brighton Ave, Portland, ME 04102", gps=(43.67651, -70.32797),
         phone="(207) 775-3318", website="https://seaglasscarwash.com", open_state="Open ⋅ Closes 7 PM",
         rating=3.6, total=263, span=900, stars=(38, 14, 10, 12, 26), honest=184, tags="car wash",
         fake=dict(scatter=14, thin=0.9, text=0.2)),
    dict(title="Pinsky's Deli", cat="deli", type="Deli", address="540 Congress St, Portland, ME 04101", gps=(43.65552, -70.26140),
         phone="(207) 773-6024", website="https://pinskysdeli.com", open_state="Closed ⋅ Opens 7 AM Mon", price="$$",
         rating=4.5, total=9840, span=60, stars=(58, 20, 8, 5, 9), honest=200, tags="deli sandwich restaurant", langs=True, owner=0.02),
    dict(title="Tidewater Coffee Roasters", cat="coffee", type="Coffee shop", address="56 Washington Ave, Portland, ME 04101", gps=(43.66510, -70.25219),
         phone="(207) 780-9917", website="https://tidewatercoffeeroasters.com", open_state="Closed ⋅ Opens 6:30 AM Mon", price="$",
         rating=4.6, total=640, span=500, stars=(64, 22, 7, 3, 4), honest=200, tags="coffee cafe", owner=0.4),
    dict(title="Lantern Books", cat="books", type="Book store", address="17 Exchange St, Portland, ME 04101", gps=(43.65689, -70.25356),
         phone="(207) 774-5108", website="https://lanternbooksme.com", open_state="Open ⋅ Closes 8 PM",
         rating=4.8, total=410, span=900, stars=(74, 18, 5, 1, 2), honest=200, tags="books bookstore", owner=0.6),
    # search results only, until someone reads them
    dict(title="Driftwood Pizza Co.", cat="pizza", type="Pizza restaurant", address="94 Ocean St, South Portland, ME 04106", gps=(43.63704, -70.25271),
         phone="(207) 799-4416", open_state="Open ⋅ Closes 9 PM", price="$$",
         rating=4.5, total=518, span=400, stars=(58, 22, 9, 4, 7), honest=190, tags="pizza restaurant", fake=dict(scatter=10, thin=0.9, text=0.3), unread=True),
    dict(title="Hilltop Slice", cat="pizza", type="Pizza Takeout", address="141 Congress St, Portland, ME 04101", gps=(43.66590, -70.24812),
         phone="(207) 772-0739", open_state="Open ⋅ Closes 11 PM", price="$",
         rating=4.3, total=176, span=700, stars=(50, 25, 10, 6, 9), honest=176, tags="pizza", unread=True),
    dict(title="Brick Oven Tavern", cat="pizza", type="Italian restaurant", address="640 Stevens Ave, Portland, ME 04103", gps=(43.68086, -70.29400),
         phone="(207) 797-2284", open_state="Open ⋅ Closes 10 PM", price="$$",
         rating=4.4, total=1203, span=300, stars=(55, 24, 10, 5, 6), honest=200, tags="pizza italian restaurant", unread=True),
    dict(title="Wharfside Pizza Bar", cat="pizza", type="Pizza restaurant", address="8 Moulton St, Portland, ME 04101", gps=(43.65639, -70.25309),
         phone="(207) 761-0583", open_state="Open ⋅ Closes 12 AM", price="$$",
         rating=4.6, total=347, span=600, stars=(64, 18, 8, 4, 6), honest=200, tags="pizza bar", unread=True),
    dict(title="Cinder & Crust", cat="pizza", type="Pizza restaurant", address="1041 Brighton Ave, Portland, ME 04102", gps=(43.67518, -70.32202),
         phone="(207) 828-4471", open_state="Closed ⋅ Opens 4 PM Mon", price="$$",
         rating=4.8, total=129, span=900, stars=(76, 14, 5, 2, 3), honest=129, tags="pizza", unread=True),
]
DETAILS = dict(food=(5, 5, 5, 4, 4, 3), service=(5, 5, 4, 4, 3, 2), atmosphere=(5, 4, 4, 4, 3))
PRICE = dict(pizza=["$10–20", "$20–30", "$20–30"], deli=["$10–20", "$10–20", "$20–30"], steak=["$50–100", "$50–100", "$100+"])
GENERIC = ["Amazing!", "Highly recommend!", "Best in Portland!", "Excellent service.", "Five stars, will be back.", "Wonderful experience, thank you!",
           "Great experience from start to finish.", "Very professional.", "The best!!", "Loved it", "Super friendly staff.", "10/10"]


def data_id(title):
    h = hashlib.sha1(title.encode()).hexdigest()
    return f"0x{h[:16]}:0x{h[16:32]}"


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def entry(p):
    """The place as google_maps returns it."""
    total, mix = p["total"], p["stars"]
    e = dict(title=p["title"], data_id=data_id(p["title"]), address=p["address"], rating=p["rating"], reviews=total, type=p["type"],
             gps_coordinates=dict(latitude=p["gps"][0], longitude=p["gps"][1]), thumbnail=f"/demo/{slugify(p['title'])}.jpg",
             open_state=p["open_state"], phone=p["phone"], rating_summary=[dict(stars=5 - i, amount=round(total * m / 100)) for i, m in enumerate(mix)])
    e.update({k: p[k] for k in ("website", "price", "description") if k in p})
    return e


class FakeApi(Api):
    """The three engines, generated. `delay` slows each call so a run can be watched."""

    def __init__(self, delay=0.0):
        self.hl, self.calls, self.cached, self.delay = "en", 0, 0, delay
        self.reviewers = {}  # contributor_id -> what their record should say
        self.generated = {}

    def account(self):
        return dict(total_searches_left=12480, account_email="you@example.com", plan_name="Developer")

    def search(self, **params):
        time.sleep(self.delay)
        self.calls += 1
        engine = params["engine"]
        if engine == "google_maps":
            q = params["q"].lower()
            exact = [p for p in PLACES if p["title"].lower() in q]
            if exact:
                return dict(place_results=entry(exact[0]))
            words = set(q.replace(",", " ").split())
            return dict(local_results=[entry(p) for p in PLACES if words & set(p["tags"].split())])
        if engine == "google_maps_reviews":
            p = next(p for p in PLACES if data_id(p["title"]) == params["data_id"])
            rs = self.reviews_of(p)
            start = int(params.get("next_page_token") or 0)
            end = start + (20 if start else 8)
            e = entry(p)
            return dict(place_info={k: e[k] for k in ("title", "address", "rating", "reviews", "type")}, reviews=rs[start:end],
                        serpapi_pagination=dict(next_page_token=str(end)) if end < len(rs) else {})
        if engine == "google_maps_contributor_reviews":
            return self.record(params["contributor_id"])
        raise ValueError(engine)

    # ---- the place's reviews ----------------------------------------------------------------------------------

    def reviews_of(self, p):
        if p["title"] not in self.generated:
            self.generated[p["title"]] = sorted(self.write(p), key=lambda r: r["iso_date"], reverse=True)
        return self.generated[p["title"]]

    def write(self, p):
        rnd = random.Random(p["title"])
        text = CORPUS[p["cat"]]
        out = []

        def name():
            first, last = rnd.choice(FIRST), rnd.choice(LAST)
            return rnd.choices([f"{first} {last}", f"{first} {last[0]}.", f"{first} {last[0]}", first.lower() + " " + last.lower(), first],
                               weights=[70, 12, 6, 6, 6])[0]

        def review(when, rating, depth, words, kind, who=None, photos=0, guide=False, likes=0):
            uid = str(10**20 + rnd.randrange(10**20))
            self.reviewers[uid] = dict(kind=kind, n=depth, place=p, rating=rating, rnd=random.Random(uid))
            r = dict(review_id=f"Ci9DQUlRQUNvZENodHljRjlvT2{uid[-10:]}{len(out)}", rating=rating, iso_date=when.strftime("%Y-%m-%dT%H:%M:%SZ"), source="Google",
                     link=f"https://www.google.com/maps/contrib/{uid}", snippet=words,
                     user=dict(name=who or name(), contributor_id=uid, reviews=depth, local_guide=guide), likes=likes)
            if photos:
                r["images"] = [f"/demo/{slugify(p['title'])}.jpg"] * photos
            if p["cat"] in PRICE and words and kind == "honest":
                d = {k: min(5, max(1, rnd.choice(v) + (rating - 4))) for k, v in DETAILS.items()}
                if rnd.random() < 0.7:
                    d["price_per_person"] = rnd.choice(PRICE[p["cat"]])
                if rnd.random() < 0.8:
                    d["meal_type"] = rnd.choice(["Lunch", "Lunch", "Dinner", "Brunch"] if p["cat"] == "deli" else ["Dinner", "Dinner", "Lunch"])
                if rnd.random() < 0.4:
                    d["wait_time"] = rnd.choice(["No wait", "Up to 10 min", "10–30 min", "10–30 min", "30–60 min"] if p["cat"] == "deli" else ["No wait", "No wait", "Up to 10 min"])
                if rnd.random() < 0.3:
                    d["noise_level"] = rnd.choice(["Loud, hard to talk", "Moderate noise", "Moderate noise", "Quiet, easy to talk"])
                if rnd.random() < 0.3:
                    d["recommended_dishes"] = ", ".join(rnd.sample(text["dishes"], rnd.randint(1, 3)))
                r["details"] = d
            if kind == "honest" and rnd.random() < p.get("owner", 0.1):
                r["response"] = dict(iso_date=(when + timedelta(hours=rnd.uniform(4, 600))).strftime("%Y-%m-%dT%H:%M:%SZ"))
            out.append(r)

        def local(day, hour=None):
            """A moment `day` days back at a local hour, in UTC."""
            hour = hour if hour is not None else rnd.choices(range(24), weights=[1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 8, 9, 8, 7, 6, 7, 8, 9, 9, 8, 6, 4, 2])[0]
            return NOW - timedelta(days=int(day)) + timedelta(hours=hour + UTC_OFFSET - NOW.hour, minutes=rnd.uniform(0, 60))

        decks = {}

        def deal(kind, n=1):
            """The next `n` lines of a shuffled pile, reshuffled when it runs out, so reviews rarely repeat each other."""
            pile = decks.setdefault(kind, [])
            got = []
            while len(got) < n:
                if not pile:
                    pile.extend(rnd.sample(text[kind], len(text[kind])))
                line = pile.pop()
                if line not in got:
                    got.append(line)
            return got

        written = []
        longs = {k: rnd.sample(text[k], len(text[k])) for k in ("long_good", "long_bad")}

        def said(rating):
            """What a real customer writes: often a line, sometimes a paragraph, the odd long story."""
            side = "good" if rating >= 4 else "bad" if rating <= 2 else "mixed"
            roll = rnd.random()
            if side != "mixed" and roll < 0.07 and longs[f"long_{side}"]:
                return longs[f"long_{side}"].pop()
            if side != "mixed" and roll < (0.45 if side == "good" else 0.2):
                return deal(f"short_{side}")[0]
            for _ in range(30):  # two reviews that share a long sentence read as copies, to the app and to anyone
                words = " ".join(deal("mixed") + deal(rnd.choice(["good", "bad"]))) if side == "mixed" else " ".join(deal(side, rnd.choice([2, 2, 3])))
                sh = signals._shingles(words)
                if all(len(sh & o) / len(sh | o) < 0.35 for o in written):
                    break
            written.append(sh)
            return words

        # honest reviewers: every depth, stars from the place's own mix, posting when customers post
        for _ in range(p["honest"]):
            depth = rnd.choices([1, rnd.randint(2, 3), rnd.randint(4, 10), rnd.randint(11, 50), rnd.randint(51, 400)], weights=[8, 10, 25, 35, 22])[0]
            rating = rnd.choices([5, 4, 3, 2, 1], weights=p["stars"])[0]
            words = said(rating) if rnd.random() < (0.95 if rating <= 2 else 0.5 if depth < 4 else 0.8) else ""  # the unhappy nearly always say why
            if words and p.get("langs") and rnd.random() < 0.2:  # visitors, in a line (under eight words, too short to echo)
                words = rnd.choice(["Très bon, mais trop d'attente.", "Excellent repas, on reviendra!", "Service rapide et sympathique.", "Muy bueno, pero un poco caro.",
                                    "Sehr gutes Essen.", "Das Fleisch war perfekt.", "Muito bom, vale a pena.", "Ottimo, anche il servizio."])
            n = len(words.split())
            likes = rnd.randint(8, 45) if n >= 50 and rnd.random() < 0.6 else rnd.randint(1, 6) if n >= 15 and rnd.random() < 0.15 else 0
            review(local(rnd.uniform(0, p["span"])), rating, depth, words, "honest", photos=rnd.random() < 0.18 and rnd.randint(1, 4),
                   guide=depth > 10 and rnd.random() < 0.5, likes=likes)

        f = p.get("fake")
        if not f:
            return out
        fake = lambda when, words: review(when, 5, 1 if rnd.random() < f["thin"] else rnd.randint(2, 3), words, "fake")
        line = lambda: rnd.choice(GENERIC) if rnd.random() < f["text"] else ""
        # a week that carries far more five-stars than the place gets, in office hours
        for day, n in f.get("bursts", []):
            for _ in range(n):
                fake(local(day - rnd.uniform(0, 6), rnd.randint(9, 16)), line())
        # spread thin across the window, some of them minutes apart
        for _ in range(f.get("scatter", 0)):
            fake(local(rnd.uniform(0, p["span"] * 0.9), rnd.randint(9, 16)), line())
        for _ in range(f.get("batches", 0)):
            t = local(rnd.uniform(0, p["span"] * 0.9), rnd.randint(9, 16))
            for k in range(3):
                fake(t + timedelta(minutes=k * rnd.uniform(1, 6)), line())
        # asked for at the table: the same waiter named, families posting together after dinner
        for i in range(f.get("table", 0) // 2):
            t, waiter, family = local(rnd.uniform(0, p["span"] * 0.9), rnd.randint(20, 22)), rnd.choice(f["staff"]), rnd.choice(LAST)
            for k in range(2):
                said_ = rnd.choice([f"Our waiter {waiter} was so kind, thank you!", f"{waiter} was wonderful, best service.", f"Our waiter {waiter} made the night special."])
                review(t + timedelta(minutes=k * rnd.uniform(1, 5)), 5, rnd.choice([1, 1, 2]), said_, "fake", who=f"{rnd.choice(FIRST)} {family}")
        # the same words, twice over
        for i in range(f.get("echo", 0)):
            base = "The best dental clinic I have ever been to, the staff are so kind and professional and the results are amazing"
            fake(local(rnd.uniform(0, p["span"] * 0.9)), base + rnd.choice(["!", ".", " thank you!", ", highly recommend."]))
        # a handful of accounts that all review the same other places
        t = local(rnd.uniform(0, p["span"] * 0.9), 11)
        for i in range(f.get("ring", 0)):
            review(t + timedelta(minutes=i * rnd.uniform(2, 8)), 5, 1, "", "ring")
        return out

    # ---- a reviewer's whole record ----------------------------------------------------------------------------

    def record(self, uid):
        who = self.reviewers[uid]
        rnd, p = who["rnd"], who["place"]
        here = dict(place_info=dict(title=p["title"], data_id=data_id(p["title"]), gps_coordinates=entry(p)["gps_coordinates"]), rating=who["rating"])
        jitter = lambda la, lo: (la + rnd.uniform(-0.05, 0.05), lo + rnd.uniform(-0.05, 0.05))
        if who["kind"] == "ring":
            ring = [("Shoreline Smile Studio", (40.71, -74.01)), ("Pearl Ridge Dental Lab", (40.73, -73.99)), ("Bright Path Orthodontics", (40.69, -73.98))]
            others = [(t, 5, at) for t, at in ring]
        elif who["kind"] == "fake":
            city = rnd.choice(ELSEWHERE_CITIES)
            others = [(f"{rnd.choice(LAST)} {rnd.choice(['Plumbing', 'Auto Body', 'Movers', 'Roofing', 'Law Office', 'HVAC'])}", 5, jitter(*city)) for _ in range(who["n"] - 1)]
        else:
            # a landmark or two in common with other locals, the rest their own, mostly around town
            pool = [rnd.choice(list(NEAR))] * (who["n"] > 1 and rnd.random() < 0.7) + [rnd.choice(list(FAR))] * (who["n"] > 3 and rnd.random() < 0.3)
            others = [(t, rnd.choices([5, 4, 3, 2, 1], weights=[45, 30, 12, 6, 7])[0], NEAR.get(t) or FAR[t]) for t in pool]
            others += [(f"{rnd.choice(LAST)}'s {rnd.choice(['Market', 'Grill', 'Garage', 'Salon', 'Pharmacy', 'Hardware'])} #{rnd.randrange(999)}", rnd.choice([5, 4, 4, 3]),
                        jitter(*p["gps"]) if rnd.random() < 0.8 else jitter(*rnd.choice(ELSEWHERE_CITIES))) for _ in range(max(0, who["n"] - 1 - len(pool)))]
        hist = [here] + [dict(place_info=dict(title=t, data_id=data_id(t), gps_coordinates=dict(latitude=at[0], longitude=at[1])), rating=r) for t, r, at in others[:199]]
        return dict(contributor=dict(contributions=dict(reviews=who["n"], ratings=who["n"])), reviews=hist)


def photos():
    out = REPORTS / "demo"
    out.mkdir(parents=True, exist_ok=True)
    for f in (Path(__file__).parent / "demo").glob("*.jpg"):
        shutil.copy(f, out)


def build():
    photos()
    api = FakeApi()
    core.api_from_env = web.api_from_env = lambda hl="en": api  # the app's search and runs land here too
    for p in PLACES:
        if not p.get("unread"):
            s = core.read_place(p["title"], api=api)
            print(f"{s['tier']:>22}  {s['padded']:.0%}  {s['sample_rating']} → {s['clean_rating']}  {p['title']}")
    norms.build(REPORTS)
    (REPORTS / "reviewaudit.html").write_text(docket(REPORTS))
    api.delay = 0.15  # from here on a run takes long enough to watch
    return api


if __name__ == "__main__":
    build()
    print(f"demo home: {os.environ['REVIEWAUDIT_HOME']}")
    web.serve(port=int(sys.argv[1]) if len(sys.argv) > 1 else 8811, open_browser=False)
