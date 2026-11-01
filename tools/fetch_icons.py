"""Download the brand logos used by the Tech stack strip (Simple Icons, CC0) into content/icons/.
Run once; the build inlines them, so the published site makes no external requests.
    python tools/fetch_icons.py
"""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "icons"
OUT.mkdir(parents=True, exist_ok=True)
stack = json.loads((ROOT / "content" / "techstack.json").read_text(encoding="utf-8"))["items"]

for item in stack:
    got = None
    for slug in item.get("icons", []):
        url = f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg"
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                data = r.read()
            (OUT / f"{item['id']}.svg").write_bytes(data)
            got = slug
            break
        except Exception:
            continue
    print(f"{item['name']:<22} {'icon ' + got if got else 'no logo (text badge)'}")
