"""SerpApi calls behind a disk cache, so a place is paid for once and the report can be re-rendered for free."""

import hashlib
import json
import os
from pathlib import Path

import serpapi

CACHE = Path(os.environ.get("SINCERE_CACHE", ".cache"))


class Api:
    def __init__(self, api_key, hl="en"):
        self.client = serpapi.Client(api_key=api_key)
        self.hl = hl
        self.calls = 0  # paid
        self.cached = 0  # served from disk

    def search(self, **params):
        params.setdefault("hl", self.hl)
        key = hashlib.sha1(json.dumps(params, sort_keys=True).encode()).hexdigest()[:16]
        path = CACHE / f"{params['engine']}-{key}.json"
        if path.exists():
            self.cached += 1
            return json.loads(path.read_text())
        data = self.client.search(**params).as_dict()
        if "error" in data and "hasn't returned any results" not in data["error"]:  # no results is an answer (a hidden profile, say)
            raise RuntimeError(f"{params['engine']}: {data['error']}")
        self.calls += 1
        if params["engine"] != "google_maps_reviews" or data.get("reviews"):  # an empty page is a Google hiccup, not a fact
            CACHE.mkdir(exist_ok=True)
            path.write_text(json.dumps(data))
        return data

    def place(self, query):
        """A Maps search. An exact hit comes back as `place_results`; a broad one as `local_results` (first wins)."""
        if query.startswith("0x") and ":" in query:
            return {"data_id": query}
        data = self.search(engine="google_maps", q=query)
        place = data.get("place_results") or (data.get("local_results") or [None])[0]
        if not place:
            raise SystemExit(f"no place found for {query!r}")
        return place

    def reviews(self, data_id, limit):
        """Newest-first pages of reviews. The first page is 8 regardless of `num`; the rest 20."""
        out, token = [], None
        while len(out) < limit:
            params = dict(engine="google_maps_reviews", data_id=data_id, sort_by="newestFirst")
            if token:
                params.update(next_page_token=token, num=20)
            data = self.search(**params)
            if token and not data.get("reviews"):  # num=20 pages come back empty now and then, and SerpApi caches the empty answer
                data = self.search(**params, no_cache=True)
            if token and not data.get("reviews"):
                data = self.search(**{**params, "num": 10}, no_cache=True)
            if not out:
                self.place_info = data.get("place_info", {})
            out += data.get("reviews", [])
            token = data.get("serpapi_pagination", {}).get("next_page_token")
            if not token or not data.get("reviews"):
                break
        return out[:limit]

    def contributor(self, contributor_id):
        """Everything one account has ever reviewed (Google caps it at 200)."""
        return self.search(engine="google_maps_contributor_reviews", contributor_id=contributor_id, num=200)
