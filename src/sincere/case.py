"""Turns the analysis into a case: findings in order of strength, each with its evidence, and what was ruled out."""

from collections import Counter


def _pct(x):
    return f"{x:.0%}"


def _when(w, years):
    return f"{w['start']:%-d} to {w['end']:%-d %b}" + (f" {w['end']:%Y}" if years else "")


def _link(a, b):
    staff = set(a.tells.get("names staff", "").split(", ")) & set(b.tells.get("names staff", "").split(", ")) - {""}
    if staff:
        return "both name " + ", ".join(sorted(staff))
    sa, sb = a.user_name.split()[-1].lower(), b.user_name.split()[-1].lower()
    if len(a.user_name.split()) > 1 and sa == sb:
        return "same surname"
    if not a.text and not b.text:
        return "neither wrote anything"
    if a.user_reviews <= 1 and b.user_reviews <= 1:
        return "both first reviews"
    return ""


def nature(suspects):
    """One sentence on what the taken-out reviews mostly are, when one kind dominates."""
    if len(suspects) < 5:
        return ""
    staff = sum("names staff" in r.tells for r in suspects) / len(suspects)
    bought = sum(("praise burst" in r.tells or r.user_reviews <= 1) and not r.trust for r in suspects) / len(suspects)
    if staff >= 0.4:
        return "Most of it is customers asked to review on the spot, not strangers for hire."
    if bought >= 0.5:
        return "Most of it looks bought: first-time accounts with nothing much to say, arriving together."
    return ""


def build(place, reviews, result, checked):
    fives = [r for r in reviews if r.rating == 5]
    years = len({r.date.year for r in reviews}) > 1
    findings, ruled_out = [], []

    # 1. who gives the five stars
    d, base, excess = result["depth"], result["base_share"], result["excess"]
    first = d[0]
    if base is not None and first["n"] >= 5:
        gap = first["share"] - base
        if excess >= 3 and gap >= 0.08:
            findings.append(dict(
                id="depth",
                strength="strong" if gap >= 0.15 and first["n"] >= 20 else "moderate",
                title="Reviewers with no record like it more than anyone else",
                claim=f"{first['n']} of the last {len(reviews)} reviews come from accounts reviewing for the first time, and {first['fives']} of those are five stars ({_pct(first['share'])}). "
                      f"Accounts with 4 to 50 reviews give the same place five stars {_pct(base)} of the time. "
                      f"Had the first-timers rated like them, there would be {excess} fewer five-star reviews.",
                exhibit="depth",
            ))
        else:
            ruled_out.append(f"First-time reviewers and accounts with a record give it five stars at about the same rate ({_pct(first['share'])} against {_pct(base)}, {first['n']} first-timers).")
        deep = d[-1]
        if deep["n"] >= 10 and base - deep["share"] >= 0.15:
            findings.append(dict(
                id="seasoned", strength="moderate",
                title="The most seasoned reviewers are the least impressed",
                claim=f"{deep['n']} reviews come from accounts with more than 50 reviews. {_pct(deep['share'])} of them are five stars, against {_pct(base)} from accounts with 4 to 50 and {_pct(first['share'])} from first-timers. The more places an account has seen, the lower it rates this one.",
            ))
    elif base is None:
        ruled_out.append("Too few reviews from accounts with a record to set a baseline for first-time reviewers.")

    # 2. bursts
    for name, word in (("praise burst", "five"), ("attack burst", "one")):
        ws = result["bursts"].get(name, [])
        if not ws:
            ruled_out.append(f"No week carried an unusual run of {word}-star reviews.")
            continue
        rows = []
        for w in ws:
            m = w["members"]
            busiest = Counter(r.date.date() for r in m).most_common(1)[0]
            rows.append([_when(w, years), str(w["n"]), f"{w['expected']:g}", f"{busiest[1]} on {busiest[0]:%-d %b}", str(sum(r.user_reviews <= 1 for r in m)), str(sum(not r.text for r in m)), str(sum(r.photos > 0 for r in m))])
        total = sum(w["n"] for w in ws)
        members = [r for w in ws for r in w["members"]]
        rest = [r for r in reviews if r.rating == (5 if word == "five" else 1) and r not in members]
        photo_rest = sum(r.photos > 0 for r in rest) / len(rest) if rest else 0
        findings.append(dict(
            id=name.replace(" ", "-"),
            strength="strong" if total >= 20 or len(ws) >= 2 else "moderate",
            title=f"{'One week' if len(ws) == 1 else str(len(ws)) + ' weeks'} carried far more {word}-star reviews than this place gets",
            claim=f"A normal week here brings {ws[0]['expected']:g} {word}-star review{'s' if ws[0]['expected'] != 1 else ''}. "
                  + " ".join(f"{_when(w, years)} brought {w['n']}." for w in ws)
                  + f" Of the {total}, {sum(r.user_reviews <= 1 for r in members)} were first-time reviewers and {sum(r.photos > 0 for r in members)} carried a photo"
                  + (f", against {_pct(photo_rest)} of the other {word}-star reviews." if rest else "."),
            table=dict(head=["week", "reviews", "normal", "busiest day", "first-timers", "no text", "photos"], rows=rows),
            exhibit="timeline",
        ))

    # 3. minutes apart
    c = result["close"]
    if c["flagged"]:
        tight = c["pairs"][:5]
        kinds = []
        if c["staff"] >= 3:
            kinds.append(f"{c['staff']} of the {c['members']} name a member of staff, which is what a table asked to review before the bill looks like")
        if c["family"] >= 2:
            kinds.append(f"{c['family']} pairs share a surname, so the same party is being counted twice")
        if c["thin"] >= 3:
            kinds.append(f"{c['thin']} are first-time reviewers with no text, which is what a batch upload looks like")
        findings.append(dict(
            id="minutes", strength="strong",
            title="Five-star reviews arrive in batches, minutes apart",
            claim=f"{c['observed']} five-star reviews were posted within ten minutes of the previous one. At this place's pace, allowing for the hours of the day people post, that should happen about {c['expected']:g} times in {len(fives)} reviews. "
                  + ("Independent customers do not queue up. " + "; ".join(kinds) + "." if kinds else "Independent customers do not queue up."),
            table=dict(head=["gap", "first", "second", "when", "what links them"], rows=[[f"{g:.0f} min" if g >= 1 else "< 1 min", a.user_name, b.user_name, f"{a.date:%-d %b %Y, %H:%M} UTC", _link(a, b)] for a, b, g in tight]),
        ))
    elif c["observed"]:
        ruled_out.append(f"{c['observed']} five-star reviews came within ten minutes of another; {c['expected']:g} would be expected from the hours people post here, so not out of line.")
    else:
        ruled_out.append("No two five-star reviews were posted within ten minutes of each other.")

    # 3b. staff named
    staff = result["staff"]
    named = [r for r in reviews if "names staff" in r.tells]
    if named and len(named) / len(reviews) >= 0.15:
        share5 = sum(r.rating == 5 for r in named) / len(named)
        top = ", ".join(f"{n} in {k}" for n, k in staff.most_common(4))
        findings.append(dict(
            id="staff", strength="moderate",
            title="Reviews name the staff: asked for on the spot",
            claim=f"{len(named)} of the {len(reviews)} reviews name a member of staff ({top}). {_pct(share5)} of those are five stars. "
                  "A named waiter, doctor or guide is the mark of a review written at the request of that person, usually before leaving. Real customers, not an independent sample.",
        ))
    elif named:
        ruled_out.append(f"Only {len(named)} reviews name a member of staff, so the place is not running its ratings through the people at the counter.")

    # 4. echoes
    if result["echoes"]:
        n = sum(len(cl) for cl in result["echoes"])
        findings.append(dict(
            id="echo", strength="strong",
            title="Reviews that say the same thing in the same words",
            claim=f"{n} reviews share at least half of their three-word phrases with another review of this place. People who were there write differently; a script does not.",
            exhibit="echoes",
        ))
    else:
        ruled_out.append(f"No two of the {sum(1 for r in reviews if len(r.text.split()) >= 8)} reviews with real text repeat each other's wording.")

    # 5. what the records showed
    if checked:
        only_here = [r for r in checked if r.history["n"] <= 1]
        praise = [r for r in checked if "only praises" in r.tells]
        rings = [r for r in checked if "ring" in r.tells]
        brand = [r for r in checked if "brand loyal" in r.tells]
        facts = [f"{len(only_here)} had reviewed nothing but this place", f"{len(praise)} have given five stars to everything they ever rated"]
        if brand:
            facts.append(f"{len(brand)} review other {place['title'].split()[0]} locations")
        if rings:
            findings.append(dict(
                id="ring", strength="strong",
                title="A group of accounts keeps reviewing the same places",
                claim=f"{len(rings)} of the {len(checked)} accounts looked up share two or more other places with at least two others in the group: " + "; ".join(f"{r.user_name} ({r.tells['ring']})" for r in rings[:4]) + ". Strangers do not do that.",
            ))
        else:
            ruled_out.append(f"None of the {len(checked)} accounts looked up form a group that reviews the same other places (two that do are usually a couple; it takes three).")
        findings.append(dict(
            id="records", strength="weak" if not praise and not only_here else "moderate",
            title=f"What the {len(checked)} reviewer records showed",
            claim=f"The reviewers most worth a look had their whole Google history read. Of them, " + ", ".join(facts) + ". "
                  "Neither is proof on its own; both are what bought reviews look like, and the exhibits below carry them.",
        ))

    # 6. drift
    if place.get("rating") and result["sample_rating"] is not None:
        drift = result["sample_rating"] - place["rating"]
        if abs(drift) >= 0.3:
            findings.append(dict(
                id="drift", strength="weak",
                title=f"Recent reviews run {abs(drift):.1f} stars {'above' if drift > 0 else 'below'} the lifetime rating",
                claim=f"Google shows {place['rating']} from all {place.get('reviews', 0):,} reviews; the last {len(reviews)} average {result['sample_rating']}. "
                      + ("Either the place got better, or the praise did." if drift > 0 else "Either the place got worse, or the older praise was the padding."),
            ))

    order = {"strong": 0, "moderate": 1, "weak": 2}
    findings.sort(key=lambda f: order[f["strength"]])
    return findings, ruled_out, nature(result["suspects"])
