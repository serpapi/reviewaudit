<h1 align="center">
  <img src="docs/icon.png" width="76" alt=""><br>
  reviewaudit
</h1>

<p align="center"><b>Is this 4.8 real?</b><br>
Reads a Google Maps place's reviews and tells you how much of the praise its own reviewers can explain.</p>

<p align="center">
  <a href="https://github.com/serpapi/reviewaudit/actions/workflows/test.yml"><img src="https://github.com/serpapi/reviewaudit/actions/workflows/test.yml/badge.svg" alt="tests"></a>
  <img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/license-MIT-black" alt="MIT">
  <a href="https://serpapi.com"><img src="https://img.shields.io/badge/data-SerpApi-6b46d9" alt="SerpApi"></a>
</p>

<p align="center"><img src="docs/report.png" alt="A case: an invented dinner cruise that looks manufactured" width="900"></p>

Every business with a rating has an incentive to improve it, and a market that will sell it
one. reviewaudit reads the newest reviews of one place through [SerpApi](https://serpapi.com),
pulls the full Google record of the reviewers worth a closer look, and writes a single page
that says which reviews the place's own baseline cannot explain, what the rating is without
them, and what kind of padding it is: bought, or asked for at the table.

**It reports patterns worth investigating, not findings.** Every number is a statistic over
public reviews, set against the place's own reviewers and the other places read. It says where
a place's reviews behave unusually and how much of its rating that pattern accounts for. It
does not establish that any particular review is fake, or who wrote it; that is why every
verdict reads "looks".

The page above is Harbor Lights Dinner Cruise, which does not exist. Every place, review and
reviewer in these images is invented by `tools/demo.py`, with the padding written in: first-time
accounts that give five stars far more often than reviewers with a record, and two weeks that
each brought over 30 five-star reviews where a normal week brings four. Taken out, they move
the recent rating from 4.3 to 3.9.

Every one of those claims is on the page with the chart or table it came from, and every
review taken out is listed with a link back to Google.

It runs on your machine with your own SerpApi key. A place costs about 42 credits and two
minutes. The free plan's 250 searches a month read five places.

```sh
uv tool install git+https://github.com/serpapi/reviewaudit
reviewaudit serve
```

That opens `http://localhost:8811`. Paste your key from
[serpapi.com/manage-api-key](https://serpapi.com/manage-api-key), search for a place, press
**Read the reviews**.

---

## What it tells you

**Reviewers with no record like it more than anyone else.** The share of five stars from
accounts reviewing for the first time, against the share from accounts with 4 to 50 reviews
at the *same place*. The gap, not the count, is the finding.

**A week carried far more five-star reviews than this place gets.** Judged against the
sample's own median week: a Poisson tail below 0.001 and at least 2.5× the usual.

**Five-star reviews arrive in batches, minutes apart.** More pairs within ten minutes than
the hours people actually post at would predict, so a lunch rush is not mistaken for a batch.
Whether they name the same waiter, or share a surname, says which kind of batch it is.

**Reviews that say the same thing in the same words.** Texts sharing half their three-word
phrases with another review of the same place.

**A group of accounts keeps reviewing the same places.** Three or more of the checked
accounts that pairwise share other places. Two is a couple on holiday.

**Nobody ever gives it four stars.** Real places collect a four-star tail: the customer who
enjoyed it but waited, or would come back but not rave. A wall of fives with nothing beside
it means the reviews are being chosen before they are written, by whoever is asked.

None of these condemns a review on its own. What gets taken out is only the *excess* over
what the place's own reviewers explain, and every review taken out is listed with a link
back to Google so you can disagree.

Below the audit, the same reviews read as reviews: what people praise and what they complain
about, Google's own review topics, sub-ratings for food, service and atmosphere with and
without the reviews taken out, what people recommend ordering, the hour of day reviews are
posted, the language mix and whether the reviewers are locals or visitors, where else they
go, how fast the owner replies and to whom, and the reviews other people found most useful.

<p align="center"><img src="docs/insights.png" alt="What the reviews say: praise and complaints, sub-ratings, posting hours, who reviews, the owner" width="900"></p>

<p align="center"><i>Anchor Street Deli, invented too: the same reviews, read as reviews.</i></p>

Each case is one self-contained HTML file, light and dark, with Open Graph tags so a pasted
link previews properly, and a print stylesheet.

## Using it

<p align="center"><img src="docs/home.png" alt="Home: search, and the cases read so far" width="900"></p>

Search Google Maps for the place (one credit, and repeats are free: everything is cached),
optionally near a city. Places you have already read open their case instead of spending
credits again:

<p align="center"><img src="docs/search.png" alt="Search results from Google Maps" width="900"></p>

The read runs in the background and reports each stage, so you can watch where the credits
go:

<p align="center"><img src="docs/run.png" alt="A read in progress" width="900"></p>

Cases are kept and compared. Once you have read eight places of your own, the "beside other
places" table on every case switches from the shipped baseline to yours:

<p align="center"><img src="docs/cases.png" alt="The cases, most padded first" width="900"></p>

A rating that does not move is not the same as a clean one: at a place where every review is
five stars, removing 42 of them leaves 5.0. What changed is how many of those stars have a
person behind them.

From the terminal, the same read:

```sh
export SERPAPI_KEY=…
reviewaudit "<place name> <city>"
reviewaudit 0x88f505b69e94a0bf:0x847b2884185db12 --reviews 400 --lookups 50
reviewaudit --norms       # rebuild the baseline and the case index from your own cases
```

Cases, cache, runs and your key live in `~/.reviewaudit` (`REVIEWAUDIT_HOME` moves it).
Nothing leaves your machine except the SerpApi calls.

## How it reads a place

Three SerpApi engines, about 42 calls:

| step | engine | what it gives |
|---|---|---|
| 1 | [`google_maps`](https://serpapi.com/google-maps-api) | the place: `data_id`, photo, description, hours, and Google's lifetime star counts |
| 2 | [`google_maps_reviews`](https://serpapi.com/google-maps-reviews-api) ×10 | the 200 newest reviews, each with the reviewer's lifetime review count, Local Guide status, photos, sub-ratings and an ISO timestamp |
| 3 | [`google_maps_contributor_reviews`](https://serpapi.com/google-maps-contributor-reviews-api) ×30 | everything the reviewers worth checking have ever reviewed, with the place behind each rating |

The cheap tells run first, so the paid record lookups go to the reviewers they point at.
Every response is cached, so re-reading a place or rebuilding its page costs nothing.

## Where it is blind

Printed on every case, because they matter:

- A place where everyone gives five stars looks the same whether they mean it or not. The
  gradient across account depth is the evidence; a flat 95% is not.
- A first review at a famous place is normal. A thin account alone never counts.
- Two accounts that share other places are usually a couple. Rings need three.
- "Newest first" still surfaces old reviews edited recently; they are shown but kept off the
  time axis.
- Hotels carry Tripadvisor and Trip.com reviews with no account behind them. They are left
  out, and the page says how many.
- 200 reviews at a very busy place can be two weeks. The case says so when the window is
  short; `--reviews 600` reads further back.

A verdict is a reading of public evidence, not an accusation. Treat it as a reason to look
closer.

## Notes for SerpApi users

- `google_maps_reviews` sometimes answers a `next_page_token` request with no reviews and
  `status: "Success"`, for a place whose previous page was full. Because the status is a
  success the empty answer is cached for the hour, so a plain retry keeps returning it;
  `no_cache=true` on the same parameters returns the page. `api.py` retries that way.
- The contributor engine returns relative dates only ("a week ago"); the reviews engine has
  `iso_date`. So the timing tells run on the place's reviews, and the contributor record is
  used for *what* an account has reviewed, not when.
- `user.reviews` on a review counts written reviews; the full record adds rating-only
  entries, so a "1 review" account can have 19 ratings. The record wins.
- `location` on `google_maps` is resolved through SerpApi's Locations API and 400s on
  anything it does not know; falling back to putting the city in `q` covers the rest.

## Development

```sh
git clone https://github.com/serpapi/reviewaudit && cd reviewaudit
uv sync
uv run pytest                      # the tells on synthetic data, the app's routes
uv run reviewaudit serve --reload  # the app, restarting when the code changes
```

```
src/reviewaudit/api.py        cached SerpApi calls, pagination, the empty-page retry
src/reviewaudit/signals.py    the tells, the baseline excess, suspect selection
src/reviewaudit/case.py       findings with evidence, what was ruled out, the kind of padding
src/reviewaudit/insights.py   what the reviews say: words, sub-ratings, hours, who, the owner
src/reviewaudit/core.py       one place end to end, with progress
src/reviewaudit/report.py     chart geometry (timeline swarm, bars, map tile), rendering
src/reviewaudit/web.py        the app: search, runs, cases
src/reviewaudit/templates/    the case page, the app pages, one stylesheet
```

`tools/overflow.js`, pasted into the console on the cases page, loads every case at five
widths and lists anything that leaks out of its card. `tools/demo.py` serves the app over an
invented Google Maps, and `tools/screenshots.py` retakes the images in `docs/` against it, so
no real place or reviewer ever appears in them.

Issues and pull requests are welcome, especially new tells with a rationale, and stop-word
lists or staff-name patterns for languages beyond English and Turkish.

## License

MIT. Review data belongs to Google and its reviewers; this reads it through SerpApi under
their terms. How you use what it finds, and whether you publish it, is yours to judge: nothing
here suggests that every use of Google Maps review data is free of legal risk.
