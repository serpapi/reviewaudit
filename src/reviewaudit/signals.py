"""The tells. Each one is a plain function over the sampled reviews; a review's suspicion is the noisy-OR of the
tells that fired on it, discounted by the things that are expensive to fake."""

import math
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta

# weight = how much one firing of the tell moves a review toward "not a real customer"
TELLS = {
    "only review": (0.45, "this place is the only thing the account has ever reviewed"),
    "thin account": (0.25, "an account with two or three reviews in total"),
    "praise burst": (0.40, "landed in a window with far more five-star reviews than this place normally gets"),
    "attack burst": (0.40, "landed in a window with far more one-star reviews than this place normally gets"),
    "echo": (0.60, "the text overlaps heavily with another review of this place"),
    "ring": (0.70, "shares two or more other places with another reviewer checked here"),
    "only praises": (0.30, "the account's whole history is five stars"),
    "brand loyal": (0.35, "the account reviews other branches of the same brand"),
    "rating only": (0.20, "stars with no text: the cheapest review there is"),
    "minutes apart": (0.40, "posted within ten minutes of another review of this place"),
    "names staff": (0.15, "mentions a member of staff by name, the mark of a review asked for on the spot"),
}
# trust = how much a costly-to-fake trait discounts the suspicion
TRUST = {
    "local guide": 0.35,
    "photos": 0.20,
    "long text": 0.15,
    "deep account": 0.40,
}


@dataclass
class Review:
    id: str
    rating: int
    date: datetime
    text: str
    user_id: str
    user_name: str
    user_reviews: int
    local_guide: bool
    photos: int
    link: str
    text_en: str = ""  # Google's translation when the review is not in the requested language
    details: dict = field(default_factory=dict)  # food/service/atmosphere, price_per_person, recommended_dishes…
    likes: int = 0
    response_at: datetime | None = None  # when the owner answered
    tells: dict = field(default_factory=dict)  # name -> detail
    trust: list = field(default_factory=list)
    history: dict | None = None

    @property
    def score(self):
        s = 1 - math.prod(1 - TELLS[t][0] for t in self.tells)
        return round(s * math.prod(1 - TRUST[t] for t in self.trust), 3)


def parse(raw):
    """One Google review. Hotels carry Tripadvisor and Trip.com reviews too; those have no account behind them."""
    u = raw["user"]
    if "contributor_id" not in u:
        return None
    text = (raw.get("extracted_snippet") or {}).get("original") or raw.get("snippet") or ""
    return Review(
        id=raw["review_id"],
        rating=int(raw["rating"]),
        date=datetime.fromisoformat(raw["iso_date"].replace("Z", "+00:00")),
        text=text,
        user_id=u["contributor_id"],
        user_name=u["name"],
        user_reviews=u.get("reviews", 0),
        local_guide=bool(u.get("local_guide")),
        photos=len(raw.get("images") or []),
        link=raw["link"],
        text_en=(raw.get("extracted_snippet") or {}).get("translated") or raw.get("snippet") or "",
        details=raw.get("details") or {},
        likes=raw.get("likes") or 0,
        response_at=datetime.fromisoformat(raw["response"]["iso_date"].replace("Z", "+00:00")) if raw.get("response", {}).get("iso_date") else None,
    )


def account_tells(reviews):
    for r in reviews:
        if r.user_reviews <= 1:
            r.tells["only review"] = "their only review"
        elif r.user_reviews <= 3:
            r.tells["thin account"] = f"{r.user_reviews} reviews in total"
        if not r.text:
            r.tells["rating only"] = "no text"
        r.trust = [t for t, ok in (("local guide", r.local_guide), ("photos", r.photos > 0), ("long text", len(r.text.split()) >= 40), ("deep account", r.user_reviews >= 50)) if ok]


def poisson_tail(k, mu):
    """P(X >= k) for X ~ Poisson(mu)."""
    if mu <= 0:
        return 0.0 if k > 0 else 1.0
    p, term = 0.0, math.exp(-mu)
    for i in range(k):
        p += term
        term *= mu / (i + 1)
    return max(0.0, 1 - p)


def bursts(reviews, rating, window=7, alpha=1e-3):
    """Sliding windows where `rating` arrives far faster than the sample's own rate says it should."""
    hits = sorted((r for r in reviews if r.rating == rating), key=lambda r: r.date)
    if len(hits) < 4:
        return []
    # "newest first" still carries edited old reviews, so the baseline is the median window, not count/span
    counts = [sum(1 for r in hits[i:] if r.date < hits[i].date + timedelta(days=window)) for i in range(len(hits))]
    rate = max(sorted(counts)[len(counts) // 2], 0.5)
    found, i = [], 0
    while i < len(hits):
        k = counts[i]
        p = poisson_tail(k, rate)
        if k >= 4 and k >= 2.5 * rate and p < alpha:
            members = hits[i : i + k]
            found.append(dict(start=hits[i].date, end=members[-1].date, n=k, expected=rate, p=p, members=members))
            i += k
        else:
            i += 1
    return found


def burst_tells(reviews):
    out = {}
    for rating, name in ((5, "praise burst"), (1, "attack burst")):
        found = bursts(reviews, rating)
        for b in found:
            for r in b["members"]:
                r.tells[name] = f"{b['n']} {'five' if rating == 5 else 'one'}-star reviews in {(b['end'] - b['start']).days + 1} days, {b['expected']} expected"
        out[name] = found
    return out


ROLE_BEFORE = r"(?:waiter|waitress|server|host|hostess|manager|chef|barista|guide|captain|driver|doctor|dr|dentist|nurse|surgeon|assistant|coordinator|translator|interpreter|consultant|staff|garson|şef|doktor|hemşire|kaptan|rehber|tercüman|danışman|usta)\.?\s+(?:named\s+|called\s+|mr\.?\s+|ms\.?\s+)?"
PRONOUNS = {"this", "that", "they", "she", "he", "we", "it", "there", "everything", "everyone", "everybody", "all", "our", "the", "food", "service", "staff", "place", "also", "and", "but", "very", "highly", "great", "overall", "nothing", "someone", "people", "team", "hotel", "restaurant", "clinic", "doctor", "dr"}
HONORIFIC = r"\s+(?:bey|hanım|hanim|abi|abla|usta|hoca|chef|şef)[^\W\d_]*"  # Turkish suffixes: abimiz, beyin
VERB = r"\s+(?:was|is|were|gave|took|served|helped|made|looked|explained|did|went|has|had|welcomed|treated)\b"


def staff_names(reviews, place_title, place_address=""):
    """People named in the text, validated by a role next to the name at least twice ("Dalyan bey", "our waiter Gökmen",
    "Dr Asil", "Silvia was"). A named waiter, doctor or guide is the mark of a review asked for on the spot."""
    fold = lambda t: unicodedata.normalize("NFKD", t.lower().replace("ı", "i")).encode("ascii", "ignore").decode()
    skip = {fold(t) for t in re.findall(r"\w+", place_title + " " + place_address)} | PRONOUNS
    name = r"([^\W\d_][^\W\d_]{2,})"
    seen = Counter()
    for r in reviews:
        found = set(re.findall(ROLE_BEFORE + name, r.text, re.I)) | set(re.findall(name + HONORIFIC, r.text)) | set(re.findall(r"(?<=[a-zçğıöşü] )" + name + VERB, r.text))
        seen.update(w for w in found if w[0].isupper() and fold(w) not in skip)
    names = {w for w, n in seen.items() if n >= 2}
    by_name = Counter()
    for r in reviews:
        hit = [w for w in names if re.search(rf"(?<![^\W\d_]){re.escape(w)}(?![^\W\d_])", r.text)]
        if hit:
            r.tells["names staff"] = ", ".join(sorted(hit))
            by_name.update(hit)
    return by_name


def close_pairs(reviews, rating=5, minutes=10):
    """Reviews of one rating posted within `minutes` of each other. Expected count is hour-of-day aware, so a lunch
    place's 13:30 rush does not read as a batch upload."""
    hits = sorted((r for r in reviews if r.rating == rating), key=lambda r: r.date)
    if len(hits) < 5:
        return dict(observed=0, expected=0.0, pairs=[], flagged=False)
    dates = sorted(r.date for r in reviews)
    days = len({d.date() for d in dates[len(dates) // 10 :]})  # active days in the dense window; edited-years-ago reviews don't count
    per_hour = Counter(r.date.hour for r in hits)
    expected = sum(1 - math.exp(-minutes * per_hour[r.date.hour] / (days * 60)) for r in hits[:-1])
    pairs = [(a, b, (b.date - a.date).total_seconds() / 60) for a, b in zip(hits, hits[1:]) if (b.date - a.date).total_seconds() <= minutes * 60]
    for a, b, gap in pairs:
        for r in (a, b):
            r.tells["minutes apart"] = f"{gap:.0f} min from another five-star" if gap >= 1 else "under a minute from another five-star"
    members = {r.id: r for a, b, _ in pairs for r in (a, b)}.values()
    surname = lambda r: r.user_name.split()[-1].lower() if len(r.user_name.split()) > 1 else None
    staff = sum("names staff" in r.tells for r in members)
    family = sum(1 for a, b, _ in pairs if surname(a) and surname(a) == surname(b))
    ratio = len(pairs) / expected if expected else 0
    # busy honest places run 1-2x the hourly model (people post after the meal, together); a batch is 4x, or 2.5x
    # when the pairs themselves say why they are pairs (the same waiter named, the same surname)
    flagged = len(pairs) >= 5 and (ratio >= 4 or (ratio >= 2.5 and staff + family >= 3))
    return dict(
        observed=len(pairs), expected=round(expected, 1), pairs=sorted(pairs, key=lambda t: t[2]), flagged=flagged,
        members=len(members), staff=staff, family=family, thin=sum(r.user_reviews <= 1 and not r.text for r in members),
    )


def _shingles(text, n=3):
    words = re.sub(r"[^\w\s]", " ", text.lower()).split()
    return {" ".join(words[i : i + n]) for i in range(len(words) - n + 1)}


def echo_tells(reviews, threshold=0.5):
    """Near-duplicate texts, clustered."""
    sh = {r.id: _shingles(r.text) for r in reviews if len(r.text.split()) >= 8}
    parent = {i: i for i in sh}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    ids = list(sh)
    pairs = []
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            sa, sb = sh[ids[a]], sh[ids[b]]
            j = len(sa & sb) / len(sa | sb)
            if j >= threshold:
                pairs.append((ids[a], ids[b], j))
                parent[find(ids[a])] = find(ids[b])
    clusters = defaultdict(list)
    by_id = {r.id: r for r in reviews}
    for a, b, j in pairs:
        for x in (a, b):
            r = by_id[x]
            r.tells["echo"] = f"{int(j * 100)}% of its phrasing appears in another review"
    for x in sh:
        if find(x) != x or any(find(y) == x for y in sh if y != x):
            clusters[find(x)].append(by_id[x])
    return [sorted(c, key=lambda r: r.date) for c in clusters.values() if len(c) > 1]


def brand_key(title):
    return re.sub(r"[^\w]", "", title.split()[0].lower()) if title else ""


def history_tells(reviews, histories, place_data_id, place_title):
    """`histories` maps user_id -> contributor response. Reads each account's whole record for the three history tells."""
    brand = brand_key(place_title)
    places_by_user = {}
    for r in reviews:
        h = histories.get(r.user_id)
        if not h:
            continue
        hist = [x for x in h.get("reviews", []) if "place_info" in x]  # a few old entries come without a place
        others = [x for x in hist if x["place_info"].get("data_id") != place_data_id]
        r.history = dict(
            n=len(hist),
            ratings=Counter(int(x["rating"]) for x in hist if "rating" in x),
            places=[x["place_info"].get("title", "?") for x in others],
            gps=[(x["place_info"]["gps_coordinates"]["latitude"], x["place_info"]["gps_coordinates"]["longitude"]) for x in others if x["place_info"].get("gps_coordinates")],
            contributions=h.get("contributor", {}).get("contributions", {}),
        )
        places_by_user[r.user_id] = {x["place_info"]["data_id"] for x in others if x["place_info"].get("data_id")}
        # `user.reviews` counts written reviews only; the full record may show the account is not thin after all
        if len(hist) >= 2:
            r.tells.pop("only review", None)
        if len(hist) >= 4:
            r.tells.pop("thin account", None)
        rated = [int(x["rating"]) for x in hist if "rating" in x]
        if len(rated) >= 3 and rated.count(5) / len(rated) >= 0.9:
            r.tells["only praises"] = f"{rated.count(5)} of {len(rated)} ratings are five stars"
        same = [p for p in r.history["places"] if brand and brand_key(p) == brand]
        if len(same) >= 2:
            r.tells["brand loyal"] = f"also reviewed {len(same)} other {place_title.split()[0]} locations"
    # ring: three or more checked accounts that pairwise share other places (two is a couple on holiday)
    by_user = {r.user_id: r for r in reviews}
    users = list(places_by_user)
    mates = {u: [] for u in users}
    for a in range(len(users)):
        for b in range(a + 1, len(users)):
            if len(places_by_user[users[a]] & places_by_user[users[b]]) >= 2:
                mates[users[a]].append(users[b])
                mates[users[b]].append(users[a])
    for u, ms in mates.items():
        if len(ms) >= 2:
            by_user[u].tells["ring"] = "reviews the same places as " + ", ".join(by_user[m].user_name for m in ms)


def lookup_candidates(reviews, limit):
    """Who is worth a contributor call: five-star (and burst one-star) reviewers with a short but non-empty record, most suspicious first."""
    pool = [r for r in reviews if r.user_reviews <= 40 and (r.rating == 5 or "attack burst" in r.tells)]
    pool.sort(key=lambda r: (-r.score, r.user_reviews))
    return pool[:limit]


DEPTH = (("1", 1, 1), ("2-3", 2, 3), ("4-10", 4, 10), ("11-50", 11, 50), ("51+", 51, 10**9))


def depth_table(reviews):
    """Five-star share by how much the account has reviewed. The gradient is the picture; the excess is the estimate."""
    rows = []
    for label, lo, hi in DEPTH:
        g = [r for r in reviews if lo <= r.user_reviews <= hi]
        rows.append(dict(label=label, n=len(g), fives=sum(r.rating == 5 for r in g), share=(sum(r.rating == 5 for r in g) / len(g)) if g else None))
    return rows


def excess_praise(reviews, rows):
    """How many more five-stars the thin accounts gave than established accounts (4-50 reviews) would have."""
    ref = [r for r in reviews if 4 <= r.user_reviews <= 50]
    if len(ref) < 20:
        ref = [r for r in reviews if r.user_reviews >= 4]
    if len(ref) < 10:
        return 0, None
    base = sum(r.rating == 5 for r in ref) / len(ref)
    excess = sum(row["n"] * max(0.0, row["share"] - base) for row in rows[:2] if row["share"] is not None)
    return round(excess), base


def pick_suspects(reviews, excess, bursts, close):
    """Only what the place's own baseline cannot explain: the thin-account excess, each burst's excess and the
    close-pair excess, filled with the most suspicious candidates, plus every echo and ring member. Account tells
    alone never condemn a review."""
    chosen = {r.id for r in reviews if "echo" in r.tells or "ring" in r.tells}
    if close["flagged"]:
        chosen |= {r.id for a, b, _ in close["pairs"][: round(close["observed"] - close["expected"])] for r in (a, b)}
    thin = sorted((r for r in reviews if r.rating == 5 and r.user_reviews <= 3), key=lambda r: -r.score)
    chosen |= {r.id for r in thin[:excess]}
    for windows in bursts.values():
        for w in windows:
            members = sorted(w["members"], key=lambda r: -r.score)
            chosen |= {r.id for r in members[: round(w["n"] - w["expected"])]}
    return sorted((r for r in reviews if r.id in chosen), key=lambda r: -r.score)


def verdict(reviews, suspects):
    fives = [r for r in reviews if r.rating == 5]
    padded = sum(r.rating == 5 for r in suspects) / len(fives) if fives else 0
    ones = [r for r in reviews if r.rating == 1]
    attacked = sum(r.rating == 1 for r in suspects) / len(ones) if ones else 0
    tier = ("looks genuine", "lightly padded", "padded", "manufactured")[sum(padded >= t for t in (0.05, 0.15, 0.35))]
    return dict(padded=padded, attacked=attacked, tier=tier)


def analyze(reviews, histories, place_data_id, place_title, place_address=""):
    account_tells(reviews)
    burst_windows = burst_tells(reviews)
    echoes = echo_tells(reviews)
    staff = staff_names(reviews, place_title, place_address)
    close = close_pairs(reviews)
    history_tells(reviews, histories, place_data_id, place_title)
    rows = depth_table(reviews)
    excess, base = excess_praise(reviews, rows)
    suspects = pick_suspects(reviews, excess, burst_windows, close)
    kept = [r for r in reviews if r not in suspects]
    mean = lambda rs: round(sum(r.rating for r in rs) / len(rs), 2) if rs else None
    fives = [r for r in reviews if r.rating == 5]
    measures = dict(  # the place-level numbers that norms are drawn from
        first_share=rows[0]["n"] / len(reviews),
        first_gap=(rows[0]["share"] - base) if base is not None and rows[0]["share"] is not None else None,
        close_ratio=close["observed"] / close["expected"] if close["expected"] else None,
        staff_share=sum("names staff" in r.tells for r in reviews) / len(reviews),
        photo_share=sum(r.photos > 0 for r in fives) / len(fives) if fives else None,
        text_share=sum(bool(r.text) for r in fives) / len(fives) if fives else None,
        five_share=len(fives) / len(reviews),
    )
    return dict(
        verdict=verdict(reviews, suspects),
        measures=measures,
        sample_rating=mean(reviews),
        clean_rating=mean(kept),
        suspects=suspects,
        depth=rows,
        excess=excess,
        base_share=base,
        bursts=burst_windows,
        close=close,
        staff=staff,
        echoes=echoes,
        tell_counts=Counter(t for r in reviews for t in r.tells),
    )
