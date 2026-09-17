"""Where reviewaudit keeps things: one folder, yours, overridable with REVIEWAUDIT_HOME."""

import json
import os
from pathlib import Path

HOME = Path(os.environ.get("REVIEWAUDIT_HOME", "~/.reviewaudit")).expanduser()
CACHE, REPORTS, RUNS, CONFIG = HOME / "cache", HOME / "reports", HOME / "runs", HOME / "config.json"


def config():
    try:
        return json.loads(CONFIG.read_text())
    except FileNotFoundError:
        return {}


def save_config(**kv):
    HOME.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps({**config(), **kv}, indent=1))
    CONFIG.chmod(0o600)


def api_key():
    """SERPAPI_KEY in the environment wins; otherwise what was saved through the app."""
    return os.environ.get("SERPAPI_KEY") or os.environ.get("SERPAPI_API_KEY") or config().get("api_key")
