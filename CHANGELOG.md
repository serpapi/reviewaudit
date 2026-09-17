# Changelog

## 0.1.0

First release. Reads a Google Maps place's newest reviews through SerpApi and writes one
case page: a verdict, findings with the chart or table that proves each one, what was ruled
out, the reviews taken out, and what the reviews say about the place itself.

- The app: search Google Maps (optionally near a city), start a read, watch it stage by
  stage, browse the cases. `reviewaudit serve`.
- The CLI: `reviewaudit "<place>"`, `reviewaudit --norms`.
- Tells: first-timer excess over the place's own baseline, burst weeks, batches posted
  minutes apart, repeated wording, reviewer rings, staff named in the text.
- Every case compared against the norms of the places read so far; ships with a baseline
  from 19 places across nine cities.
