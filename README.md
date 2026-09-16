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

## What it looks for

Account tells (`only review`, `thin account`, `rating only`) never condemn a review on
their own; they rank. What gets taken out is only what the place's own baseline cannot
explain:

- the five-stars from thin accounts beyond the rate that accounts with 4 to 50 reviews
  give the same place;
- the reviews in a week where one rating arrived far faster than the sample's median
  week (Poisson tail below 0.001, at least 2.5×), beyond that week's expected count;
- every member of an echo (texts sharing half their 3-word shingles) or a ring (three or
  more checked accounts that pairwise share other places).

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
src/sincere/report.py     chart geometry (timeline swarm, bars), the verdict sentence
src/sincere/templates/    one HTML page, no build step, light and dark
```

`google_maps_reviews` pages asked for with `num=20` sometimes come back empty with
`Success`, and SerpApi caches that answer for an hour; `api.py` retries with
`no_cache=true`, then falls back to `num=10`.
