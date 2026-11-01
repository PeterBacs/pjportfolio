"""Static site generator for the portfolio.

    python tools/build.py

Reads content/*.json + templates/, writes the finished site to dist/.
Optional environment variables (see .env.example):
    SITE_URL   absolute public URL, e.g. https://peter-bacani.netlify.app (enables canonical, social cards, sitemap)
    BASE_PATH  sub-path if the site is not served from the domain root, e.g. /portfolio
"""
import json
import re
import os
import shutil
import sys
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SITE_URL = (os.environ.get("SITE_URL") or os.environ.get("URL") or "").rstrip("/")
if not SITE_URL and os.environ.get("VERCEL_PROJECT_PRODUCTION_URL"):
    SITE_URL = "https://" + os.environ["VERCEL_PROJECT_PRODUCTION_URL"]
BASE = (os.environ.get("BASE_PATH") or "").rstrip("/")
# The site is private-by-obscurity by default: search engines are told not to list it. Set ALLOW_INDEXING=1 to publish it for search.
ALLOW_INDEXING = os.environ.get("ALLOW_INDEXING") == "1"

load = lambda p: json.loads((ROOT / p).read_text(encoding="utf-8"))
profile = load("content/profile.json")
# Microsoft Clarity project ID: CLARITY_ID env var wins, else content/analytics.json. Empty = analytics off.
CLARITY_ID = re.sub(r"[^A-Za-z0-9]", "", os.environ.get("CLARITY_ID") or load("content/analytics.json").get("clarityId", ""))
skills = load("content/skills.json")
registry = load("content/media.json")
manifest = load("media/manifest.json")
projects = sorted(
    (json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "content/projects").glob("*.json")),
    key=lambda p: p["featuredOrder"],
)
by_slug = {p["slug"]: p for p in projects}


import hashlib
asset_v = hashlib.md5(b"".join(p.read_bytes() for p in sorted((ROOT / "static").rglob("*")) if p.is_file() and p.suffix in (".css", ".js"))).hexdigest()[:8]


def u(path):
    return f"{BASE}{path}"


def absu(path):
    return f"{SITE_URL}{BASE}{path}" if SITE_URL else ""


def fmt_bytes(n):
    return f"{n / 1024:.0f} KB" if n < 1_000_000 else f"{n / 1_000_000:.1f} MB"


def img(key, sizes="100vw", cls="", loading="lazy", alt=None, fetchpriority=None, max_w=None):
    m = manifest["images"][key]
    vs = [v for v in m["variants"] if not max_w or v["w"] <= max_w] or m["variants"][:1]
    srcset = ", ".join(f"{u('/media/img/' + v['file'])} {v['w']}w" for v in vs)
    big = vs[-1]
    a = alt if alt is not None else registry["images"][key]["alt"]
    extra = f' fetchpriority="{fetchpriority}"' if fetchpriority else ""
    return Markup(
        f'<img src="{u("/media/img/" + big["file"])}" srcset="{srcset}" sizes="{sizes}" '
        f'width="{big["w"]}" height="{big["h"]}" alt="{escape(a)}" loading="{loading}" decoding="async"'
        f'{" class=" + chr(34) + cls + chr(34) if cls else ""}{extra}>'
    )


def full_url(key):
    return u("/media/img/" + manifest["images"][key]["variants"][-1]["file"])


def img_url(key, w=None):
    vs = manifest["images"][key]["variants"]
    pick = [v for v in vs if not w or v["w"] <= w]
    return u("/media/img/" + (pick[-1] if pick else vs[0])["file"])


def img_srcset(key):
    return ", ".join(f"{u('/media/img/' + v['file'])} {v['w']}w" for v in manifest["images"][key]["variants"])


def img_alt(key):
    return registry["images"][key]["alt"]


def doc_info(doc_id):
    d = manifest["documents"][doc_id]
    return {"url": u("/media/docs/" + d["file"]), "size": fmt_bytes(d["bytes"]), "file": d["file"]}


# ---- enrich projects ------------------------------------------------------
for i, p in enumerate(projects):
    p["url"] = u(f"/projects/{p['slug']}/")
    p["docs_resolved"] = [{**d, **doc_info(d["id"])} for d in p["docs"]]
    p["videos_resolved"] = [
        {"id": v, **manifest["videos"][v]} for v in p["videos"] if v in manifest["videos"]
    ]
    p["prev"] = projects[i - 1] if i > 0 else None
    p["next"] = projects[i + 1] if i < len(projects) - 1 else None
    p["search"] = " ".join(
        [p["name"], p["fullTitle"], p["summary"], " ".join(p["tech"]), p["keywords"], p["role"], p["status"]]
    ).lower()

all_tech = {}
for p in projects:
    for t in p["tech"]:
        all_tech[t] = all_tech.get(t, 0) + 1
tech_list = sorted(all_tech.items(), key=lambda kv: kv[0].lower())
status_list = sorted({p["statusGroup"] for p in projects})
years = sorted({p["year"] for p in projects if p.get("year")})
has_years = len(years) >= 2  # year filter and "newest" sort need at least two distinct years
featured = [p for p in projects if p["featuredOrder"] <= 4]
def _readable_text(hex_color):
    """Black or white text, whichever contrasts better with the badge colour."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    lum = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    return "#101316" if (lum + 0.05) / 0.05 > 1.05 / (lum + 0.05) else "#ffffff"


techstack = load("content/techstack.json")
awards = load("content/awards.json")
home_data = load("content/home.json")
cinema = load("content/cinema.json")
for _st in home_data["stages"]:
    _st["project_list"] = [by_slug[x] for x in _st["projects"]]
_aw = {a["id"]: a for a in awards["awards"]}
home_data["recognition_items"] = [_aw[i] for i in home_data["recognition"]]
_by_id = {t["id"]: t for t in techstack["items"]}
techgroups = [{**g, "items": [_by_id[i] for i in g["ids"]]} for g in techstack["groups"]]
for _t in techstack["items"]:
    _f = ROOT / "content" / "icons" / f"{_t['id']}.svg"
    _m = re.search(r'\sd="([^"]+)"', _f.read_text(encoding="utf-8")) if _f.exists() else None
    _t["path"] = _m.group(1) if _m else None
    _t["fg"] = _readable_text(_t["color"])
roles = load("content/roles.json")["roles"]
philosophy = load("content/philosophy.json")
gallery = load("content/gallery.json")
avp = load("content/avp.json")
articles = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "content/articles").glob("*.json"))]
for r in roles:
    r["url"] = u(f"/for/{r['slug']}/")
    r["project_cards"] = [{**by_slug[x["slug"]], "why": x["why"]} for x in r["projects"]]
    r["sections"] = [s for s in skills["sections"] if s["id"] in r["skillSections"]]
for a in articles:
    a["url"] = u(f"/articles/{a['slug']}/")

# ---- jinja ----------------------------------------------------------------
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html", "xml"]),
                  trim_blocks=True, lstrip_blocks=True)
env.globals.update(
    asset_v=asset_v, clarity_id=CLARITY_ID, cinema=cinema, site_noindex=not ALLOW_INDEXING, u=u, absu=absu, img=img, img_url=img_url, img_srcset=img_srcset, img_alt=img_alt, philosophy=philosophy, gallery=gallery, avp=avp, full_url=full_url, profile=profile, projects=projects, featured=featured,
    skills=skills, site_url=SITE_URL, nav=[
        ("Home", "/", "home"), ("About", "/#about", "about"), ("Skills", "/#skills", "skills"),
        ("Projects", "/#projects", "projects"), ("Awards", "/#awards", "awards"), ("Photo Gallery", "/#gallery", "gallery"), ("Contact", "/#contact", "contact"),
    ],
    registry=registry, manifest=manifest, doc_info=doc_info, by_slug=by_slug, roles=roles, articles=articles, techstack=techstack, home_data=home_data, techgroups=techgroups, awards=awards, year=date.today().year,
    resume_pages=manifest["resume"]["pages"], ldm_pages=manifest["ldm"]["pages"], og_for=lambda k: absu("/media/img/" + manifest["og"][k]) if SITE_URL else "",
)

written = []


def render(template, out, **ctx):
    html = env.get_template(template).render(**ctx)
    target = DIST / out.lstrip("/")
    if target.suffix != ".html":
        target = target / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    written.append(out)


def main():
    if DIST.exists():
        shutil.rmtree(DIST, ignore_errors=True)  # a locked file (e.g. a video being played) is simply overwritten below
    DIST.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "static", DIST / "assets", dirs_exist_ok=True)
    # only copy the media that is referenced and published
    shutil.copytree(ROOT / "media", DIST / "media", ignore=shutil.ignore_patterns("manifest.json"), dirs_exist_ok=True)
    for f in ("_headers", "_redirects"):
        if (ROOT / "static_root" / f).exists():
            shutil.copy2(ROOT / "static_root" / f, DIST / f)

    render("home.html", "/", page="home", title="Engr. Peter John R. Bacani: Electronics Engineer",
           description="Portfolio of Peter John R. Bacani, a registered Electronics Engineer and engineering educator: embedded, IoT, applied AI and research prototypes with documented evidence.",
           og_image=og_key("home"), canonical="/")
    render("projects.html", "/projects/", page="projects", title="Projects | Engr. Peter John R. Bacani",
           description="Search and filter engineering projects in machine learning, medical imaging, wearable electronics, seismic modelling and web systems.",
           tech_list=tech_list, status_list=status_list, years=years, has_years=has_years,
           og_image=og_key("home"), canonical="/projects/")
    for p in projects:
        render("project.html", f"/projects/{p['slug']}/", page="projects", p=p,
               title=f"{p['name']} | Engr. Peter John R. Bacani", description=p["summary"],
               og_image=og_key(p["thumbnail"][6:]), canonical=f"/projects/{p['slug']}/")
    render("skills.html", "/skills/", page="skills", title="Technical Skills and Engineering Capabilities | Engr. Peter John R. Bacani",
           description="Embedded systems, robotics, applied AI, electronics design, software and research skills, each linked to the project that shows it.",
           og_image=og_key("home"), canonical="/skills/")
    render("about.html", "/about/", page="about", title="About | Engr. Peter John R. Bacani",
           description="Registered Electronics Engineer, engineering educator and research mentor: qualifications, experience, education and awards.",
           og_image=og_key("home"), canonical="/about/")
    render("awards.html", "/awards/", page="awards", title="Awards and Recognition | Engr. Peter John R. Bacani",
           description="Silver Prize at the Seoul International Invention Fair 2024, SIBOL First Prize at NICE 2024, and National Science and Technology Fair recognition, with sources.",
           og_image="home", canonical="/awards/")
    render("contact.html", "/contact/", page="contact", title="Contact | Engr. Peter John R. Bacani",
           description="Contact Engr. Peter John R. Bacani by email about engineering, research and development roles.",
           og_image=og_key("home"), canonical="/contact/")
    render("gallery.html", "/gallery/", page="gallery", title="Photo Gallery | Engr. Peter John R. Bacani",
           description="Photos of classroom learning, student research mentoring, science fairs and school events.",
           og_image="home", canonical="/gallery/")
    render("philosophy.html", "/philosophy/", page="about", title="Teaching Philosophy | Engr. Peter John R. Bacani",
           description="My teaching philosophy: learning with purpose, learning by doing, supporting every learner, and using technology with a clear purpose.",
           og_image="home", canonical="/philosophy/")
    for r in roles:
        render("role.html", f"/for/{r['slug']}/", page="", r=r, title=f"{r['nav']} | Engr. Peter John R. Bacani",
               description=r["summary"], og_image="home", canonical=f"/for/{r['slug']}/")
    for a in articles:
        render("article.html", f"/articles/{a['slug']}/", page="", a=a, title=f"{a['title']} | Engr. Peter John R. Bacani",
               description=a["description"], og_image="home", canonical=f"/articles/{a['slug']}/")
    render("404.html", "/404.html", page="", title="Page not found | Engr. Peter John R. Bacani",
           description="This page could not be found.", og_image="", canonical=None, noindex=True)

    if SITE_URL and ALLOW_INDEXING:
        urls = [w for w in written if w != "/404.html"]
        today = date.today().isoformat()
        body = "".join(f"<url><loc>{absu(w)}</loc><lastmod>{today}</lastmod></url>" for w in urls)
        (DIST / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>',
            encoding="utf-8")
        (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {absu('/sitemap.xml')}\n", encoding="utf-8")
    else:
        (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
        print("NOTE: no sitemap (indexing is off, or SITE_URL is not set).")
    print(f"Built {len(written)} pages into {DIST}")


def og_key(k):
    return k


if __name__ == "__main__":
    sys.exit(main())
