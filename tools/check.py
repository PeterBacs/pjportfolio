"""Post-build QA: every internal link, image, script, stylesheet, video and document in dist/ must exist.
Also verifies each project's thumbnail is the one registered for that project and that held-back media is absent.
    python tools/check.py
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
problems, checked = [], 0


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.imgs_no_alt = [], set(), 0

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        for k in ("href", "src", "poster", "data-src"):
            if k in a and a[k]:
                self.refs.append((tag, a[k]))
        if "srcset" in a:
            for part in a["srcset"].split(","):
                self.refs.append((tag, part.strip().split()[0]))
        if tag == "img" and "alt" not in a:
            self.imgs_no_alt += 1


pages = {}
for f in DIST.rglob("*.html"):
    p = P()
    p.feed(f.read_text(encoding="utf-8"))
    pages[f] = p

for f, p in pages.items():
    if p.imgs_no_alt:
        problems.append(f"{f.relative_to(DIST)}: {p.imgs_no_alt} <img> without alt")
    for tag, ref in p.refs:
        if re.match(r"(mailto:|tel:|https?:|javascript:|data:)", ref):
            continue
        u = urlparse(ref)
        path = unquote(u.path)
        if not path:  # in-page anchor
            if u.fragment and u.fragment not in p.ids:
                problems.append(f"{f.relative_to(DIST)}: missing anchor #{u.fragment}")
            continue
        t = DIST / path.lstrip("/")
        if t.is_dir():
            t = t / "index.html"
        checked += 1
        if not t.exists():
            problems.append(f"{f.relative_to(DIST)}: broken {tag} -> {ref}")
        elif u.fragment and t.suffix == ".html" and t in pages and u.fragment not in pages[t].ids:
            problems.append(f"{f.relative_to(DIST)}: missing anchor {ref}")

# thumbnail mapping
for pj in (ROOT / "content/projects").glob("*.json"):
    d = json.loads(pj.read_text(encoding="utf-8"))
    html = (DIST / "projects" / d["slug"] / "index.html").read_text(encoding="utf-8")
    if f"/media/img/{d['thumbnail']}-" not in html:
        problems.append(f"{d['slug']}: page does not use its thumbnail {d['thumbnail']}")
    others = re.findall(r"/media/img/(thumb-[a-z-]+)-\d+\.webp", html)
    if any(o != d["thumbnail"] for o in others):
        problems.append(f"{d['slug']}: references another project's thumbnail: {set(others)}")

# held-back media must not be shipped
reg = json.loads((ROOT / "content/media.json").read_text(encoding="utf-8"))
for k, v in reg["videos"].items():
    if not v.get("publish") and (DIST / "media" / "video" / f"{k}.mp4").exists():
        problems.append(f"held-back video shipped: {k}")

print(f"{len(pages)} pages, {checked} internal references checked")
if problems:
    print("PROBLEMS:")
    print("\n".join(" - " + x for x in problems))
    sys.exit(1)
print("OK: no broken links, assets or anchors; thumbnails match projects; held-back media not shipped.")
