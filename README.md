# sincere

Is this 4.8 real? Give it a Google Maps place; it reads the newest reviews through
[SerpApi](https://serpapi.com) and writes one page saying how much of the praise the
place's own reviewers can explain, and which reviews don't add up.

```
export SERPAPI_KEY=…
uv run sincere "Nusr-Et Steakhouse Etiler"        # → reports/nusr-et-steakhouse.html
uv run sincere 0x14cab61013b1d78b:0xc36794433940ac13 --reviews 400 --lookups 50
```

Three engines, about 40 calls per place, every response cached under `.cache/` so a
re-run or a template change costs nothing:

1. `google_maps` finds the place and its `data_id`.
2. `google_maps_reviews`, newest first, 20 a page. Each review carries the reviewer's
   lifetime review count, Local Guide status, photos and an ISO date.
3. `google_maps_contributor_reviews` for the reviewers worth a closer look: everything
   the account has ever reviewed, with the place behind each rating.

`uv run sincere --norms` folds every case under `reports/` into `norms.json` (median and
middle 80% of each measure) and writes the docket, `reports/sincere.html`. Re-run the places
afterwards (cached, free) and each report shows its numbers beside what is typical.

## What it reads like

A dashboard for one place: the verdict with the three ratings and the last 200 by stars,
the findings as a table of contents that jumps to the card proving each one, every review on
a timeline, five-star share by account depth, the pairs posted minutes apart, the place beside
every other place read so far, what was ruled out, and (collapsed) the reviews taken out and
the method with its blind spots.

## What it looks for

Account tells (`only review`, `thin account`, `rating only`) never condemn a review on
their own; they rank. What gets taken out is only what the place's own baseline cannot
explain:

- the five-stars from thin accounts beyond the rate that accounts with 4 to 50 reviews
  give the same place;
- the reviews in a week where one rating arrived far faster than the sample's median
  week (Poisson tail below 0.001, at least 2.5×), beyond that week's expected count;
- the five-stars posted within ten minutes of another, beyond what the hours people post
  at predict (hour-of-day aware, so a lunch rush is not a batch);
- every member of an echo (texts sharing half their 3-word shingles) or a ring (three or
  more checked accounts that pairwise share other places).

Two more tells say what kind of padding it is rather than how much: reviews that name a
member of staff ("Dalyan bey", "our waiter Gökmen", "Dr Asil") are the mark of a review
asked for on the spot, and pairs minutes apart that share a surname are one party counted
twice. The verdict says which dominates: customers asked at the table, or strangers for hire.

Each review's suspicion is the noisy-OR of its tells' weights, discounted by traits that
cost effort to fake (Local Guide, photos, long text, a deep record). Weights live in
`signals.py` and are printed at the bottom of every report.

Blind spots, also printed on the page: a place where everyone gives five stars looks
the same whether they mean it or not; a first review at a famous place is normal; two
accounts sharing places are usually a couple; "newest first" still surfaces old reviews
edited recently.

## Layout

```
src/sincere/api.py        cached SerpApi calls, pagination, the empty-page retry
src/sincere/signals.py    the tells, the baseline excess, suspect selection
src/sincere/case.py       findings with evidence, what was ruled out, the nature of the padding
src/sincere/report.py     chart geometry (timeline swarm, bars), rendering
src/sincere/templates/    report.html plus partials and style.css, no build step, light and dark
```

`google_maps_reviews` pages asked for with `num=20` sometimes come back empty with
`Success`, and SerpApi caches that answer for an hour; `api.py` retries with
`no_cache=true`, then falls back to `num=10`.
