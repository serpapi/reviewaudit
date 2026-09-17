import os
from pathlib import Path


def client(tmp_path, monkeypatch):
    monkeypatch.setenv("REVIEWAUDIT_HOME", str(tmp_path))
    monkeypatch.delenv("SERPAPI_KEY", raising=False)
    monkeypatch.delenv("SERPAPI_API_KEY", raising=False)
    import importlib

    from reviewaudit import paths

    importlib.reload(paths)
    from reviewaudit import core, web

    importlib.reload(core)
    importlib.reload(web)
    from fastapi.testclient import TestClient

    return TestClient(web.app)


def test_home_without_key_invites_setup(tmp_path, monkeypatch):
    c = client(tmp_path, monkeypatch)
    r = c.get("/")
    assert r.status_code == 200 and "add your SerpApi key" in r.text


def test_search_without_key_redirects_to_setup(tmp_path, monkeypatch):
    c = client(tmp_path, monkeypatch)
    r = c.get("/search?q=anything", follow_redirects=False)
    assert r.status_code == 307 and r.headers["location"] == "/setup"


def test_bad_key_is_refused(tmp_path, monkeypatch):
    c = client(tmp_path, monkeypatch)
    r = c.post("/setup", data={"api_key": "not-a-key"}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/setup?bad=1"
    assert not (Path(tmp_path) / "config.json").exists()


def test_cases_and_runs_pages_render_empty(tmp_path, monkeypatch):
    c = client(tmp_path, monkeypatch)
    assert "No runs yet" in c.get("/runs").text
    assert c.get("/cases").status_code == 200
