"""What the reviews say, beyond the audit: praise and complaints, sub-ratings, posting hours, who reviews, the owner."""

import math
import re
import unicodedata
from collections import Counter, defaultdict
from statistics import median

STOP = set("""a about above after again against all am an and any are as at be because been before being below between both but by can did do does
doing down during each few for from further had has have having he her here hers herself him himself his how i if in into is it its itself just
me more most my myself no nor not now of off on once only or other our ours ourselves out over own same she should so some such than that the
their theirs them themselves then there these they this those through to too under until up very was we were what when where which while who
whom why will with would you your yours yourself yourselves place really also get got one very good great nice well much many lot lots even
still back go went come came us they're it's i'm don't didn't can't you're we're there's ive im dont didnt cant wasnt isnt arent restaurant food
service staff time visit visited experience recommend recommended definitely highly overall everything something anything nothing bit little
around always never ever thing things day night people someone everyone amazing best don didn doesn isn wasn won couldn wouldn
shouldn aren weren hasn haven like made make right enough every actually way whole without felt took kept left said told asked
want wanted sure pretty though two three first last next""".split())


def _words(text):
    return [w for w in re.findall(r"[^\W\d_]{3,}", text.lower()) if w not in STOP]


def praise_and_complaints(reviews, n=22):
    """Words that lean four-to-five-star against one-to-two-star, by smoothed log-odds; sized by how often they appear."""
    good = Counter(w for r in reviews if r.rating >= 4 for w in set(_words(r.text_en or r.text)))
    bad = Counter(w for r in reviews if r.rating <= 2 for w in set(_words(r.text_en or r.text)))
    if sum(bad.values()) < 30:  # too few unhappy reviews for a contrast: take one-to-three-star
        bad = Counter(w for r in reviews if r.rating <= 3 for w in set(_words(r.text_en or r.text)))
    G, B = sum(good.values()) or 1, sum(bad.values()) or 1
    score = {w: math.log((good[w] + 1) / G) - math.log((bad[w] + 1) / B) for w in set(good) | set(bad) if good[w] + bad[w] >= 3}
    praise = sorted((w for w in score if score[w] > 0.4 and good[w] >= 3), key=lambda w: -good[w])[:n]
    complaints = sorted((w for w in score if score[w] < -0.4 and bad[w] >= 3), key=lambda w: -bad[w])[:n]
    return dict(praise=[(w, good[w]) for w in praise], complaints=[(w, bad[w]) for w in complaints], n_good=sum(r.rating >= 4 for r in reviews), n_bad=sum(r.rating <= 2 for r in reviews))


def most_useful(reviews):
    """The most-liked review on each side of the ledger, when anyone liked anything."""
    up = max((r for r in reviews if r.rating >= 4 and r.text and r.likes >= 2), key=lambda r: r.likes, default=None)
    down = max((r for r in reviews if r.rating <= 2 and r.text and r.likes >= 2), key=lambda r: r.likes, default=None)
    return dict(up=up, down=down)


def sub_ratings(reviews, suspects):
    """Food/service/atmosphere (or rooms/location…) means, everyone against the reviews that were taken out."""
    sus = {r.id for r in suspects}
    keys = [k for k, n in Counter(k for r in reviews for k, v in r.details.items() if isinstance(v, int)).most_common() if n >= 10]
    rows = []
    for k in keys:
        every = [r.details[k] for r in reviews if isinstance(r.details.get(k), int)]
        kept = [r.details[k] for r in reviews if isinstance(r.details.get(k), int) and r.id not in sus]
        rows.append(dict(key=k.replace("_", " "), n=len(every), mean=sum(every) / len(every), kept=sum(kept) / len(kept) if kept else None))
    facts = {}
    for k, label in (("price_per_person", "per person"), ("meal_type", "meal"), ("wait_time", "wait"), ("noise_level", "noise"), ("trip_type", "trip"), ("travel_group", "travelling")):
        c = Counter(r.details.get(k) for r in reviews if r.details.get(k))
        if c and c.most_common(1)[0][1] >= 5:
            facts[label] = c.most_common(1)[0]
    dishes = Counter(d.strip() for r in reviews for d in str(r.details.get("recommended_dishes", "")).split(",") if d.strip())
    moves = any(r["kept"] is not None and abs(r["kept"] - r["mean"]) >= 0.05 for r in rows)
    return dict(rows=rows, facts=facts, dishes=dishes.most_common(8), moves=moves)


def posting_hours(reviews, suspects, gps):
    """Reviews by hour of the day, in the place's approximate local time (from longitude), taken-out overlaid."""
    offset = round(gps["longitude"] / 15) if gps else 0
    sus = {r.id for r in suspects}
    all_h, sus_h = Counter(), Counter()
    for r in reviews:
        h = (r.date.hour + offset) % 24
        all_h[h] += 1
        if r.id in sus:
            sus_h[h] += 1
    night = sum(all_h[h] for h in range(1, 7))
    return dict(offset=offset, hours=[dict(h=h, n=all_h[h], sus=sus_h[h]) for h in range(24)], peak=max(range(24), key=lambda h: all_h[h]), night=night, total=len(reviews))


def _script(text):
    for ch in text:
        if ch.isalpha():
            name = unicodedata.name(ch, "")
            for s in ("LATIN", "CYRILLIC", "ARABIC", "HANGUL", "HIRAGANA", "KATAKANA", "CJK", "GREEK", "HEBREW", "THAI", "DEVANAGARI"):
                if name.startswith(s):
                    return {"HIRAGANA": "Japanese", "KATAKANA": "Japanese", "CJK": "Chinese", "HANGUL": "Korean", "CYRILLIC": "Cyrillic", "ARABIC": "Arabic", "GREEK": "Greek", "HEBREW": "Hebrew", "THAI": "Thai", "DEVANAGARI": "Hindi", "LATIN": "Latin"}[s]
    return None


def _latin_language(text):
    t = text.lower()
    if re.search(r"[ğışçö]", t) or re.search(r"(?<!['’])\b(ve|çok|bir|için|güzel|ama|ile)\b", t):
        return "Turkish"
    if re.search(r"[ßäöü]", t) or re.search(r"\b(und|sehr|nicht|aber|ist|das)\b", t):
        return "German"
    if re.search(r"\b(the|and|was|very|with|were|is|it|my|for|but|this|great|good|best|they|you|our|not|of|to|an|at|be|are|will|would|just|every|back|worth|really|nice|love|loved|amazing|finally)\b", t):
        return "English"
    if re.search(r"\b(muy|pero|con|para|bueno|una)\b", t) or "ñ" in t:
        return "Spanish"
    if re.search(r"\b(très|mais|avec|pour|nous|est|et|les|des|on)\b", t):
        return "French"
    if re.search(r"\b(molto|anche|con|per|una|buono)\b", t):
        return "Italian"
    if re.search(r"\b(muito|mas|com|para|uma|bom)\b", t):
        return "Portuguese"
    return "other Latin"


def who_reviews(reviews, checked, gps):
    """Language mix, Local Guides, and how far the pulled records' other reviews sit from this place."""
    langs = Counter()
    for r in reviews:
        if not r.text:
            continue
        s = _script(r.text)
        langs[_latin_language(r.text) if s == "Latin" else (s or "other")] += 1
    guides = sum(r.local_guide for r in reviews)
    far = near = 0
    for r in checked:
        pts = r.history.get("gps") or []
        if pts and gps:
            d = median(_km(gps["latitude"], gps["longitude"], la, lo) for la, lo in pts)
            far += d > 300
            near += d <= 300
    return dict(langs=langs.most_common(6), with_text=sum(1 for r in reviews if r.text), guides=guides, far=far, near=near)


def _km(la1, lo1, la2, lo2):
    p = math.pi / 180
    a = 0.5 - math.cos((la2 - la1) * p) / 2 + math.cos(la1 * p) * math.cos(la2 * p) * (1 - math.cos((lo2 - lo1) * p)) / 2
    return 12742 * math.asin(math.sqrt(a))


def where_else(checked, place_data_id, n=8):
    """The other places the pulled records reviewed most, with how many of them did."""
    c = Counter()
    for r in checked:
        for title in set(r.history.get("places", [])):
            c[title] += 1
    return [(t, k) for t, k in c.most_common(n) if k >= 2]


def owner(reviews):
    """Reply rate and speed, and whether the unhappy get answered first."""
    answered = [r for r in reviews if r.response_at]
    if not answered:
        return None
    delays = sorted((r.response_at - r.date).total_seconds() / 3600 for r in answered)
    by_star = {}
    for s in (5, 4, 3, 2, 1):
        rs = [r for r in reviews if r.rating == s]
        if rs:
            by_star[s] = sum(1 for r in rs if r.response_at) / len(rs)
    return dict(rate=len(answered) / len(reviews), median_h=delays[len(delays) // 2], by_star=by_star, n=len(answered))


def build(reviews, suspects, checked, place):
    gps = place.get("gps_coordinates")
    return dict(
        words=praise_and_complaints(reviews),
        useful=most_useful(reviews),
        subs=sub_ratings(reviews, suspects),
        hours=posting_hours(reviews, suspects, gps),
        who=who_reviews(reviews, checked, gps),
        elsewhere=where_else(checked, place.get("data_id")),
        owner=owner(reviews),
    )
