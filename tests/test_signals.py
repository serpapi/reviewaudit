from datetime import datetime, timedelta, timezone

from reviewaudit import signals
from reviewaudit.signals import Review

T0 = datetime(2026, 6, 1, 12, tzinfo=timezone.utc)


def review(i, rating=5, days=0.0, minutes=0.0, text="a perfectly ordinary review of a perfectly ordinary place", user_reviews=12, photos=0, name=None):
    return Review(id=f"r{i}", rating=rating, date=T0 + timedelta(days=days, minutes=minutes), text=text, user_id=f"u{i}",
                  user_name=name or f"User {i}", user_reviews=user_reviews, local_guide=False, photos=photos, link="")


def steady(n=60, rating=5, **kw):
    """One review a day, at a different hour each day, each saying something of its own."""
    return [review(i, rating=rating, days=i, minutes=(i * 37 * 60) % 1440, text=f"review number {i} says something of its own about visit {i * 7}", **kw) for i in range(n)]


def test_poisson_tail():
    assert signals.poisson_tail(0, 2.0) == 1.0
    assert abs(signals.poisson_tail(1, 2.0) - 0.8647) < 1e-3
    assert signals.poisson_tail(30, 2.0) < 1e-12


def test_burst_found_against_steady_baseline():
    rs = steady() + [review(100 + i, days=30, minutes=i) for i in range(20)]
    found = signals.bursts(rs, 5)
    assert len(found) == 1 and found[0]["n"] >= 20


def test_no_burst_on_steady_flow():
    assert signals.bursts(steady(), 5) == []


def test_close_pairs_flag_and_hour_awareness():
    rs = steady(200)
    assert not signals.close_pairs(rs)["flagged"]
    batch = rs + [review(500 + i, days=90, minutes=3 * i) for i in range(20)]
    c = signals.close_pairs(batch)
    assert c["flagged"] and c["observed"] >= 19


def test_echo_clusters_near_duplicates():
    a = review(1, text="Amazing food, the lamb was tender and the staff were so kind and quick")
    b = review(2, text="Amazing food, the lamb was tender and the staff were so kind and fast")
    c = review(3, text="Terrible parking situation but the view from the terrace saves it entirely")
    clusters = signals.echo_tells([a, b, c])
    assert len(clusters) == 1 and {r.id for r in clusters[0]} == {"r1", "r2"}
    assert "echo" in a.tells and "echo" not in c.tells


def test_staff_names_need_a_role_twice_and_skip_the_place():
    rs = [review(1, text="Dalyan bey was so attentive"), review(2, text="our waiter Dalyan made the night"),
          review(3, text="Thanks Nusret for the show"), review(4, text="Everything was great")]
    names = signals.staff_names(rs, "Nusret Steakhouse")
    assert dict(names) == {"Dalyan": 2}
    assert "names staff" in rs[0].tells and "names staff" not in rs[3].tells


def test_excess_praise_only_counts_the_gap():
    rs = [review(i, user_reviews=20, rating=5 if i % 2 else 4) for i in range(40)]  # established: 50% five-star
    rs += [review(100 + i, user_reviews=1, rating=5) for i in range(20)]  # first-timers: 100%
    signals.account_tells(rs)
    rows = signals.depth_table(rs)
    excess, base = signals.excess_praise(rs, rows)
    assert base == 0.5 and excess == 10


def test_account_tells_never_convict_alone():
    rs = [review(i, user_reviews=1, text="", rating=5, days=i) for i in range(10)] + steady(10, user_reviews=20)
    result = signals.analyze(rs, {}, "x", "Place")
    assert result["suspects"] == []  # thin accounts rate exactly like the established ones, so nothing is beyond baseline
