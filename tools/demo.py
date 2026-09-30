"""reviewaudit against an invented Google Maps: the README images, with no real place or reviewer in them.

    uv run python tools/demo.py [port]      # builds the demo cases in a temp home, then serves the app
    uv run python tools/screenshots.py      # in another shell

Every place, review and reviewer here is generated from a seed. `FakeApi` answers the same three engines the real
`Api` calls, in the same shapes, so the read, the case pages and the app are the real code over synthetic data. The
padding in each place is written in on purpose (a first-timer surge, bursts, minute-apart batches, a named waiter,
echoes, a ring) so every tell has something to find.
"""

import hashlib
import os
import random
import re
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone

os.environ["REVIEWAUDIT_HOME"] = tempfile.mkdtemp(prefix="reviewaudit-demo-")
os.environ["SERPAPI_KEY"] = "demo"

from reviewaudit import core, norms, web  # noqa: E402  (after the home is set)
from reviewaudit.api import Api  # noqa: E402
from reviewaudit.paths import REPORTS  # noqa: E402
from reviewaudit.report import docket  # noqa: E402

NOW = datetime(2026, 9, 20, 18, tzinfo=timezone.utc)
TOWN = "Port Arden, ME 04999"

FIRST = "Alex Sam Jordan Maria Priya Tom Grace Leo Nina Omar Ruth Ben Clara Ivan Mei Jonah Lucia Ahmed Hana Paul Rosa Ethan Zoe Dev Lena Marco Ada Felix Iris Kofi Noor Owen Tess Yusuf Elena Ravi Maya Hugo Anya Theo".split()
LAST = "Keller Brooks Nakamura Ortiz Lindqvist Moreau Patel Whitfield Adeyemi Novak Castillo Hughes Tanaka Fischer Rahman Doyle Silva Kowalski Mendez Park Olsen Varga Quinn Haddad Sato Byrne Costa Weber Singh Duarte".split()

DETAILS = dict(food=(5, 5, 5, 4, 4, 3), service=(5, 5, 4, 4, 3, 2), atmosphere=(5, 4, 4, 4, 3))
TEXT = {
    "cruise": dict(
        good=["The sunset over the harbor was stunning.", "Dinner was better than expected for a boat.", "Crew kept the drinks coming all evening.",
              "Great views of the lighthouse on the way back.", "Live music on the top deck made the night.", "The seafood platter was fresh and generous."],
        bad=["Overpriced for what you get.", "The food was cold and the portions small.", "Boarding was chaotic and we waited forty minutes.",
             "Crowded deck, no seats unless you paid extra.", "Loud speakers made talking impossible.", "The advertised menu was not what they served."]),
    "pizza": dict(
        good=["The margherita is the real thing, blistered crust and bright sauce.", "Wood oven pizza worth the drive.", "Friendly staff and quick service.",
              "The garlic knots are addictive.", "Best crust in town, chewy and light.", "Cozy room, perfect for a family dinner."],
        bad=["Waited an hour for a pizza that came out burnt.", "Soggy middle and bland sauce.", "Rude at the counter when we asked about our order.",
             "Too salty, and the toppings were sparse.", "Overpriced for the size."]),
    "deli": dict(
        good=["The pastrami sandwich is enormous and worth every bite.", "Rye bread is baked in house and you can tell.", "Classic deli, the line moves fast.",
              "Matzo ball soup like my grandmother made.", "Huge portions, bring a friend.", "The pickles alone are worth the trip.", "Cheerful counter staff who remember regulars."],
        bad=["The line was long and the counter staff were curt.", "Paid a fortune for a dry sandwich.", "Tables were sticky and the floor dirty.",
             "They forgot half the order and would not refund it.", "Bread was stale and the meat fatty.", "Cash only, which nobody told us until the end.",
             "Noisy, cramped, and they rush you out."]),
    "dental": dict(
        good=["Painless cleaning and a very gentle hygienist.", "They explained every step before doing it.", "Modern clinic, spotless and calm.",
              "Got me in the same day for an emergency.", "Front desk sorted my insurance without fuss.", "The dentist took time to answer every question.", "My kids are no longer scared of the dentist.", "Crown fitted perfectly on the first try.", "Reminders by text so I never miss a cleaning."],
        bad=["Billed for work they never mentioned.", "Waited an hour past my appointment.", "Pushed expensive treatments I did not need."]),
    "towing": dict(
        good=["Arrived in twenty minutes at night.", "Driver was careful with my car.", "Fair price and no surprises.", "Called back right away and kept me updated.", "Towed my van across town for a fair flat rate.", "Polite dispatcher who stayed on the line with me.", "They took card payment right at the roadside.", "Saved us on a freezing night after a breakdown."],
        bad=["Charged double the quote.", "Took three hours to show up.", "Scratched my bumper and denied it."]),
    "steak": dict(
        good=["Ribeye cooked exactly as ordered.", "Excellent wine list and a helpful sommelier.", "Warm room, great for a celebration.", "The creamed spinach is a must."],
        bad=["Steak was overcooked and they argued about it.", "Very expensive for average food.", "Service was slow on a quiet night."]),
    "locksmith": dict(
        good=["Opened my door in five minutes without damage.", "Honest price, quoted on the phone.", "Rekeyed the whole house the same afternoon.", "Fixed a sticky deadbolt in ten minutes flat.", "Cut spare keys while I waited, cheap and exact.", "Came out at midnight when I was locked out.", "Installed a smart lock and showed me how it works.", "Explained every option without pushing the dearest one."],
        bad=["Quoted one price and charged another.", "Never showed up after two calls."]),
    "carwash": dict(
        good=["Interior came out spotless.", "Quick and friendly.", "Good value on the monthly plan.", "Tire shine and windows done without asking.", "The hand dryers leave no streaks at all.", "Friendly attendants who guide you onto the track.", "Pet hair gone from every seat."],
        bad=["Left water spots all over the hood.", "Scratched the paint and would not pay for it.", "Waited forty minutes on a weekday.", "Vacuum missed half the car."]),
    "coffee": dict(
        good=["Beans roasted on site and it shows.", "Best flat white in town.", "Quiet in the mornings, good for working.", "Friendly baristas who know their coffee.", "The cardamom bun is worth the queue.", "Oat milk at no extra charge.", "Big windows and plenty of plugs by the tables.", "They sell their own beans by the bag.", "Cold brew is smooth and strong."],
        bad=["Pricey and the pastries were stale.", "Wifi never works."]),
    "books": dict(
        good=["A proper bookshop with staff who read.", "Great secondhand section.", "Lovely reading nook upstairs.", "They ordered in a rare title for me in two days.", "The poetry shelf is better than any in the city.", "Staff picks on every table, and they are good.", "Children's corner kept my son busy for an hour.", "Readings on Thursday nights with local authors.", "Wrapped a gift for me without asking."],
        bad=["Prices are higher than online.", "Cramped aisles and nowhere to sit.", "Staff ignored me at the till for ages."]),
}
ELSEWHERE = ["Port Arden Farmers Market", "Harbor Point Lighthouse", "Arden Public Library", "Quay Street Bakery", "Gull Island Ferry", "Pinecrest Trailhead",
             "Arden Cinema", "Saltmarsh Brewing", "Northside Hardware", "Hillcrest Diner", "Tidepool Aquarium", "Arden Train Station"]
SYN = {  # swaps that keep the sentence grammatical and its sentiment where it was
    "great": ["excellent", "fantastic", "lovely"], "best": ["finest", "top"], "friendly": ["welcoming", "warm"], "fresh": ["just made", "very fresh"],
    "quick": ["fast", "speedy"], "fast": ["quickly", "briskly"], "huge": ["massive", "big"], "enormous": ["gigantic", "huge"], "worth": ["well worth"],
    "rude": ["unfriendly", "dismissive"], "cold": ["lukewarm", "not hot"], "dirty": ["grimy", "filthy"],
    "was": ["was", "was really"], "were": ["were", "were very"], "and": ["and", "and also"], "we": ["we", "my family"],
    "stale": ["dry", "old"], "expensive": ["pricey", "overpriced"], "staff": ["team"], "perfect": ["ideal", "just right"],
}
ADJ = set("""fresh generous real bright friendly quick addictive chewy light cozy burnt soggy bland rude salty sparse
fast cheerful curt dry sticky dirty stale fatty noisy cramped gentle calm spotless modern careful fair expensive slow warm helpful honest quiet
lovely cold small chaotic crowded loud overpriced long overcooked average great good""".split())
FAR = ["Riverside Motel", "Summit Ski Lodge", "Lakeview Campground", "Downtown Transit Center", "Maple Grove Mall", "Airport Parking East"]

# spec: category, the honest reviewers' star mix, how far back 200 reviews reach, and what padding is written in
PLACES = [
    dict(title="Harbor Lights Dinner Cruise", cat="cruise", type="Cruise agency", emoji="🛥️", color=("#1e2a4a", "#3b4f8a"), street="Pier 4, Harbor Road",
         rating=4.7, total=1057, span=880, stars=(52, 16, 10, 6, 16), honest=118, tags="cruise boat dinner harbor",
         fake=dict(bursts=[(520, 34), (400, 33)], scatter=14, thin=0.85, text=0.25)),
    dict(title="Nonna Lucia Pizzeria", cat="pizza", type="Pizza restaurant", emoji="🍕", color=("#7a2e1d", "#c8553d"), street="41 Market Street",
         rating=4.7, total=232, span=700, stars=(62, 18, 8, 5, 7), honest=150, tags="pizza italian restaurant",
         fake=dict(table=36, staff=["Marco", "Giulia"], thin=0.8, text=0.9)),
    dict(title="Bayside Towing & Recovery", cat="towing", type="Towing service", emoji="🚚", color=("#3d3d3d", "#e0a526"), street="9 Industrial Way",
         rating=5.0, total=286, span=900, stars=(94, 3, 1, 1, 1), honest=150, tags="towing",
         fake=dict(scatter=34, batches=10, thin=0.9, text=0.3)),
    dict(title="Brightwater Dental", cat="dental", type="Dentist", emoji="🦷", color=("#1f6f78", "#7fc8c2"), street="220 Elm Avenue",
         rating=4.9, total=312, span=760, stars=(82, 8, 3, 2, 5), honest=160, tags="dentist dental",
         fake=dict(scatter=18, echo=16, ring=6, thin=0.5, text=1.0)),
    dict(title="Old Mill Steakhouse", cat="steak", type="Steak house", emoji="🥩", color=("#4a2c1f", "#9a5b3a"), street="3 Mill Lane",
         rating=4.4, total=2140, span=120, stars=(60, 20, 8, 5, 7), honest=170, tags="steak restaurant",
         fake=dict(scatter=30, thin=0.9, text=0.3)),
    dict(title="Keel & Key Locksmith", cat="locksmith", type="Locksmith", emoji="🔑", color=("#5a4a1a", "#c9a227"), street="17 Rope Walk",
         rating=4.9, total=894, span=1000, stars=(88, 6, 2, 1, 3), honest=182, tags="locksmith",
         fake=dict(scatter=8, batches=6, thin=0.9, text=0.4)),
    dict(title="Seaglass Car Wash", cat="carwash", type="Car wash", emoji="🚗", color=("#1d4e89", "#5fa8d3"), street="880 Coast Highway",
         rating=3.6, total=263, span=900, stars=(38, 14, 10, 12, 26), honest=184, tags="car wash",
         fake=dict(scatter=14, thin=0.9, text=0.2)),
    dict(title="Anchor Street Deli", cat="deli", type="Delicatessen", emoji="🥪", color=("#6b3e26", "#d9a066"), street="12 Anchor Street",
         rating=4.5, total=9840, span=60, stars=(58, 20, 8, 5, 9), honest=200, tags="deli sandwich restaurant", langs=True, owner=0.02),
    dict(title="Tidewater Coffee Roasters", cat="coffee", type="Coffee shop", emoji="☕", color=("#3b2a20", "#8c6a4f"), street="5 Wharf Street",
         rating=4.6, total=640, span=500, stars=(64, 22, 7, 3, 4), honest=200, tags="coffee cafe", owner=0.4),
    dict(title="Lantern Books", cat="books", type="Book store", emoji="📚", color=("#2f4a3a", "#7ea172"), street="66 High Street",
         rating=4.8, total=410, span=900, stars=(74, 18, 5, 1, 2), honest=200, tags="books bookstore", owner=0.6),
    # search results only, until someone reads them
    dict(title="Driftwood Pizza Co.", cat="pizza", type="Pizza restaurant", emoji="🍕", color=("#5c3a21", "#b07a4f"), street="7 Beach Road",
         rating=4.5, total=518, span=400, stars=(58, 22, 9, 4, 7), honest=190, tags="pizza restaurant", fake=dict(scatter=10, thin=0.9, text=0.3), unread=True),
    dict(title="Slice of Arden", cat="pizza", type="Pizza takeout", emoji="🍕", color=("#8a3b12", "#e07a3f"), street="150 Main Street",
         rating=4.3, total=176, span=700, stars=(50, 25, 10, 6, 9), honest=176, tags="pizza", unread=True),
    dict(title="Brick Oven Tavern", cat="pizza", type="Italian restaurant", emoji="🧱", color=("#6e2b24", "#b9584a"), street="28 Tavern Square",
         rating=4.4, total=1203, span=300, stars=(55, 24, 10, 5, 6), honest=200, tags="pizza italian restaurant", unread=True),
    dict(title="Quay Street Pizza Bar", cat="pizza", type="Pizza restaurant", emoji="🍕", color=("#4b2e39", "#a45a7a"), street="3 Quay Street",
         rating=4.6, total=347, span=600, stars=(64, 18, 8, 4, 6), honest=200, tags="pizza bar", unread=True),
    dict(title="Ember & Crust", cat="pizza", type="Pizza restaurant", emoji="🔥", color=("#5a1f1f", "#d0643b"), street="90 Foundry Lane",
         rating=4.8, total=129, span=900, stars=(76, 14, 5, 2, 3), honest=129, tags="pizza", unread=True),
]


def data_id(title):
    h = hashlib.sha1(title.encode()).hexdigest()
    return f"0x{h[:16]}:0x{h[16:32]}"


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def entry(p):
    """The place as google_maps returns it."""
    total, mix = p["total"], p["stars"]
    return dict(title=p["title"], data_id=data_id(p["title"]), address=f"{p['street']}, {TOWN}", rating=p["rating"], reviews=total, type=p["type"],
                thumbnail=f"/demo/{slugify(p['title'])}.svg", open_state="Open ⋅ Closes 10 PM", phone="(207) 555-01" + str(10 + PLACES.index(p)),
                website=f"https://{slugify(p['title'])}.example", rating_summary=[dict(stars=5 - i, amount=round(total * m / 100)) for i, m in enumerate(mix)])


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
        text = TEXT[p["cat"]]
        names = iter(rnd.sample([f"{f} {l}" for f in FIRST for l in LAST], 400))
        out = []

        def review(when, rating, depth, words, kind, name=None, photos=0, guide=False):
            uid = str(10**20 + rnd.randrange(10**20))
            self.reviewers[uid] = dict(kind=kind, n=depth, place=p, rating=rating, rnd=random.Random(uid))
            r = dict(review_id=f"demo{len(out)}{uid[-6:]}", rating=rating, iso_date=when.strftime("%Y-%m-%dT%H:%M:%SZ"), source="Google",
                     link=f"https://www.google.com/maps/contrib/{uid}", snippet=words,
                     user=dict(name=name or next(names), contributor_id=uid, reviews=depth, local_guide=guide), likes=0)
            if photos:
                r["images"] = ["/demo/photo.svg"] * photos
            if p["cat"] in ("pizza", "deli", "steak") and words and kind == "honest":
                r["details"] = {k: min(5, max(1, rnd.choice(v) + (rating - 4))) for k, v in DETAILS.items()}
                r["details"].update(price_per_person="$20–30", meal_type=rnd.choice(["Lunch", "Lunch", "Dinner"]), wait_time="10–30 min", noise_level="Loud, but you can still talk")
            if kind == "honest" and rnd.random() < p.get("owner", 0.1):
                r["response"] = dict(iso_date=(when + timedelta(hours=rnd.uniform(4, 600))).strftime("%Y-%m-%dT%H:%M:%SZ"))
            if kind == "honest" and len(words.split()) >= 12 and rnd.random() < 0.12:
                r["likes"] = rnd.randint(2, 40)
            out.append(r)

        def local(day, hour=None):
            hour = hour if hour is not None else rnd.choices(range(24), weights=[1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 8, 9, 8, 7, 6, 7, 8, 9, 9, 8, 6, 4, 2])[0]
            return NOW - timedelta(days=int(day)) + timedelta(hours=hour - NOW.hour, minutes=rnd.uniform(0, 60))

        def asides():
            """Two sentences of the reviewer's own, so reviews making the same point do not read as copies. The slots are
            digits and everything else a stop word, so they never reach the word cloud."""
            n = lambda lo, hi: rnd.randint(lo, hi)
            return rnd.sample([f"Visited on {n(1, 12)}/{n(1, 28)} with {n(2, 9)} of us.", f"We got there around {n(1, 9)}:{n(10, 59)}.", f"Went back on {n(1, 12)}/{n(1, 28)} too."], 2)

        def vary(sentence):
            """People say the same thing in their own words: a synonym here, a "really" before an adjective there."""
            out = []
            for i, w in enumerate(sentence.split()):
                if i and w.strip(".,!") in ADJ and out[-1].split()[-1] not in ("really", "very", "so") and rnd.random() < 0.8:
                    out.append(rnd.choice(["really", "very", "so"]))
                out.append(rnd.choice(SYN[w]) if w in SYN and rnd.random() < 0.8 else w)
            return " ".join(out)

        def said(rating):
            if rating >= 4:
                core_ = [rnd.choice(text["good"])]
            elif rating == 3:
                core_ = [rnd.choice(text["good"]), rnd.choice(text["bad"])]
            else:
                core_ = rnd.sample(text["bad"], min(2, len(text["bad"])))
            parts = [vary(s) for s in core_] + asides()
            rnd.shuffle(parts)
            return " ".join(parts)

        # honest reviewers: every depth, stars from the place's own mix, posting when customers post
        for _ in range(p["honest"]):
            depth = rnd.choices([1, rnd.randint(2, 3), rnd.randint(4, 10), rnd.randint(11, 50), rnd.randint(51, 400)], weights=[8, 10, 25, 35, 22])[0]
            rating = rnd.choices([5, 4, 3, 2, 1], weights=p["stars"])[0]
            words = said(rating) if rnd.random() < (0.5 if depth < 4 else 0.8) else ""
            if words and p.get("langs") and rnd.random() < 0.25:  # visitors, in a line or so (under eight words, too short to echo)
                words = rnd.choice(["Muy bueno, pero mucha cola.", "El pastrami, increíble.", "Très bon, mais trop d'attente.", "Le meilleur sandwich de la ville.",
                                    "Sehr gutes Pastrami.", "Das Brot ist frisch und gut.", "Molto buono, anche il pane.", "Muito bom, vale a pena."])
            review(local(rnd.uniform(0, p["span"])), rating, depth, words, "honest", photos=rnd.random() < 0.18 and rnd.randint(1, 4), guide=depth > 10 and rnd.random() < 0.5)

        f = p.get("fake")
        if not f:
            return out
        generic = ["Amazing!", "Great experience, highly recommend.", "Best in town!", "Excellent service.", "Five stars, will be back.", "Wonderful, thank you!"]
        fake = lambda when, words: review(when, 5, 1 if rnd.random() < f["thin"] else rnd.randint(2, 3), words, "fake")
        # a week that carries far more five-stars than the place gets, in office hours
        for day, n in f.get("bursts", []):
            for _ in range(n):
                fake(local(day - rnd.uniform(0, 6), rnd.randint(9, 16)), rnd.choice(generic) if rnd.random() < f["text"] else "")
        # spread thin across the window, some of them minutes apart
        for _ in range(f.get("scatter", 0)):
            fake(local(rnd.uniform(0, p["span"] * 0.9), rnd.randint(9, 16)), rnd.choice(generic) if rnd.random() < f["text"] else "")
        for _ in range(f.get("batches", 0)):
            t = local(rnd.uniform(0, p["span"] * 0.9), rnd.randint(9, 16))
            for k in range(3):
                fake(t + timedelta(minutes=k * rnd.uniform(1, 6)), rnd.choice(generic) if rnd.random() < f["text"] else "")
        # asked for at the table: the same waiter named, families posting together after dinner
        for i in range(f.get("table", 0) // 2):
            t, waiter, family = local(rnd.uniform(0, p["span"] * 0.9), rnd.randint(20, 22)), rnd.choice(f["staff"]), rnd.choice(LAST)
            for k in range(2):
                line = rnd.choice([f"Our waiter {waiter} was so kind, thank you!", f"{waiter} was wonderful, best service.",
                                   f"Our waiter {waiter} made the night special."])
                review(t + timedelta(minutes=k * rnd.uniform(1, 5)), 5, rnd.choice([1, 1, 2]), line, "fake", name=f"{rnd.choice(FIRST)} {family}")
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
        here = dict(place_info=dict(title=p["title"], data_id=data_id(p["title"])), rating=who["rating"])
        if who["kind"] == "ring":
            others = [("Arden Smile Studio", 5), ("Coastline Orthodontics", 5), ("Pearl Dental Lab", 5)]
        elif who["kind"] == "fake":
            others = [(f"{rnd.choice(LAST)} {rnd.choice(['Plumbing', 'Auto Body', 'Movers', 'Roofing', 'Law Office'])}", 5) for _ in range(who["n"] - 1)]
        else:
            # a landmark or two in common with other locals, the rest their own
            pool = [rnd.choice(ELSEWHERE)] * (who["n"] > 1 and rnd.random() < 0.7) + [rnd.choice(FAR)] * (who["n"] > 3 and rnd.random() < 0.3)
            others = [(t, rnd.choices([5, 4, 3, 2, 1], weights=[45, 30, 12, 6, 7])[0]) for t in pool]
            others += [(f"{rnd.choice(LAST)}'s {rnd.choice(['Market', 'Grill', 'Garage', 'Salon', 'Pharmacy', 'Hotel'])} #{rnd.randrange(999)}", rnd.choice([5, 4, 4, 3]))
                       for _ in range(max(0, who["n"] - 1 - len(pool)))]
        hist = [here] + [dict(place_info=dict(title=t, data_id=data_id(t)), rating=r) for t, r in others[:199]]
        return dict(contributor=dict(contributions=dict(reviews=who["n"], ratings=who["n"])), reviews=hist)


def thumbnails():
    out = REPORTS / "demo"
    out.mkdir(parents=True, exist_ok=True)
    for p in PLACES:
        a, b = p["color"]
        (out / f"{slugify(p['title'])}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs><rect width="200" height="200" fill="url(#g)"/>'
            f'<text x="100" y="128" font-size="92" text-anchor="middle">{p["emoji"]}</text></svg>')
    (out / "photo.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10" fill="#ccc"/></svg>')


def build():
    thumbnails()
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
