"""The tool: search for a place, start a read, watch it run, open the case. FastAPI over the same core the CLI uses."""

import json
import secrets
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from serpapi.exceptions import HTTPError

from . import norms
from .core import NoKey, api_from_env, cases, read_place
from .paths import REPORTS, RUNS, api_key, save_config
from .report import docket, env

STAGES = [("place", "Find the place"), ("reviews", "Read the newest reviews"), ("records", "Pull reviewer records"), ("analysis", "Weigh the tells"), ("done", "Write the case")]

app = FastAPI(title="reviewaudit")
pool = ThreadPoolExecutor(max_workers=2)
jobs, lock = {}, threading.Lock()


def page(name, **ctx):
    ctx.setdefault("account", account())
    return HTMLResponse(env.get_template(name).render(generated=datetime.now().strftime("%-d %B %Y"), has_key=bool(api_key()), **ctx))


account_cache = {}


def account():
    """Credits left, refreshed at most once a minute; None when there is no key or SerpApi is unreachable."""
    if not api_key():
        return None
    if account_cache.get("t", 0) > time.time() - 60:
        return account_cache["a"]
    try:
        a = api_from_env().account()
        account_cache.update(t=time.time(), a=a)
        return a
    except Exception:
        return account_cache.get("a")


def by_data_id():
    return {c["data_id"]: c for c in cases(REPORTS)}


# ---- jobs --------------------------------------------------------------------------------------------------------

def save(job):
    RUNS.mkdir(parents=True, exist_ok=True)
    (RUNS / f"{job['id']}.json").write_text(json.dumps(job, ensure_ascii=False))


def run_job(job):
    def say(stage, done, total, note):
        with lock:
            job["stage"], job["done"], job["total"], job["note"] = stage, done, total, note
            job["log"].append(dict(t=time.time(), stage=stage, done=done, total=total, note=note))
            save(job)

    with lock:
        job["status"], job["started"] = "running", time.time()
    try:
        summary = read_place(job["query"], reviews=job["reviews"], lookups=job["lookups"], progress=say)
        norms.build(REPORTS)
        (REPORTS / "reviewaudit.html").write_text(docket(REPORTS))
        with lock:
            job.update(status="done", result=summary, finished=time.time())
    except Exception as e:  # the page shows it; nothing else to do with it here
        with lock:
            job.update(status="error", error=f"{type(e).__name__}: {e}", finished=time.time())
    save(job)


def start(query, place=None, reviews=200, lookups=30):
    job = dict(id=secrets.token_hex(4), query=query, place=place or {}, reviews=reviews, lookups=lookups, status="queued", created=time.time(),
               stage="place", done=0, total=1, note="queued", log=[])
    with lock:
        jobs[job["id"]] = job
    save(job)
    pool.submit(run_job, job)
    return job


def load_jobs():
    for p in sorted(RUNS.glob("*.json")) if RUNS.exists() else []:
        j = json.loads(p.read_text())
        if j["status"] in ("queued", "running"):  # the process died under it
            j.update(status="error", error="interrupted", finished=time.time())
        jobs[j["id"]] = j


load_jobs()


# ---- routes ------------------------------------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home():
    recent = sorted(jobs.values(), key=lambda j: -j["created"])[:5]
    return page("home.html", cases=cases(REPORTS)[:12], running=[j for j in recent if j["status"] in ("queued", "running")])


@app.get("/setup", response_class=HTMLResponse)
def setup_page(bad: int = 0):
    return page("setup.html", bad=bad)


@app.post("/setup")
def setup_save(api_key_value: str = Form(alias="api_key")):
    key = api_key_value.strip()
    try:
        from .api import Api

        Api(key).account()
    except Exception:
        return RedirectResponse("/setup?bad=1", status_code=303)
    save_config(api_key=key)
    account_cache.clear()
    return RedirectResponse("/", status_code=303)


@app.get("/search", response_class=HTMLResponse)
def search(q: str = "", near: str = ""):
    q, near = q.strip(), near.strip()
    if not q:
        return RedirectResponse("/")
    try:
        api = api_from_env()
    except NoKey:
        return RedirectResponse("/setup")
    try:
        data = api.search(engine="google_maps", q=q, location=near, z=12) if near else api.search(engine="google_maps", q=q)
    except (RuntimeError, HTTPError):  # a place SerpApi's location list does not know (400): let Google read it from the query
        data = api.search(engine="google_maps", q=f"{q} {near}")
    hits = [data["place_results"]] if data.get("place_results") else data.get("local_results", [])
    known = by_data_id()
    for h in hits:
        h["case"] = known.get(h.get("data_id"))
    return page("search.html", q=q, near=near, hits=hits, cost=api.calls)


@app.post("/runs")
def create_run(q: str = Form(...), title: str = Form(""), thumbnail: str = Form(""), address: str = Form(""), rating: str = Form(""), reviews: int = Form(200), lookups: int = Form(30)):
    if not api_key():
        return RedirectResponse("/setup", status_code=303)
    job = start(q, place=dict(title=title, thumbnail=thumbnail, address=address, rating=rating), reviews=reviews, lookups=lookups)
    return RedirectResponse(f"/runs/{job['id']}", status_code=303)


@app.get("/runs/{job_id}", response_class=HTMLResponse)
def run_page(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(404)
    return page("run.html", job=job, stages=STAGES)


@app.get("/runs/{job_id}/status")
def run_json(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(404)
    with lock:
        return JSONResponse({k: v for k, v in job.items() if k != "log"} | {"log": job["log"][-8:]})


@app.get("/runs", response_class=HTMLResponse)
def runs_page():
    return page("runs.html", jobs=sorted(jobs.values(), key=lambda j: -j["created"]), stages=dict(STAGES))


@app.get("/cases", response_class=HTMLResponse)
@app.get("/reviewaudit.html", response_class=HTMLResponse)
def cases_page():
    return page("cases.html", cases=cases(REPORTS))


REPORTS.mkdir(parents=True, exist_ok=True)
app.mount("/", StaticFiles(directory=REPORTS), name="reports")


def serve(port=8811, open_browser=True):
    import socket
    import webbrowser

    import uvicorn

    host = socket.gethostname().split(".")[0]
    print(f"reviewaudit is at http://localhost:{port}  (from another machine: http://{host}:{port})")
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")
