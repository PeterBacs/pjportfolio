"""One-off: wire role pages, the method article and the skills glance into the site."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rw(p, f):
    path = ROOT / p
    s = path.read_text(encoding="utf-8")
    path.write_text(f(s), encoding="utf-8", newline="\n")


def w(p, text):
    (ROOT / p).write_text(text, encoding="utf-8", newline="\n")


# ---- build.py
def bld(s):
    if "roles = " in s:
        return s
    s = s.replace('featured = [p for p in projects if p["featuredOrder"] <= 4]', '''featured = [p for p in projects if p["featuredOrder"] <= 4]
roles = load("content/roles.json")["roles"]
articles = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "content/articles").glob("*.json"))]
for r in roles:
    r["url"] = u(f"/for/{r['slug']}/")
    r["project_cards"] = [{**by_slug[x["slug"]], "why": x["why"]} for x in r["projects"]]
    r["sections"] = [s for s in skills["sections"] if s["id"] in r["skillSections"]]
for a in articles:
    a["url"] = u(f"/articles/{a['slug']}/")''')
    s = s.replace("by_slug=by_slug, year=date.today().year,", "by_slug=by_slug, roles=roles, articles=articles, year=date.today().year,")
    s = s.replace('    render("404.html"', '''    for r in roles:
        render("role.html", f"/for/{r['slug']}/", page="", r=r, title=f"{r['nav']} | Engr. Peter John R. Bacani",
               description=r["summary"], og_image="home", canonical=f"/for/{r['slug']}/")
    for a in articles:
        render("article.html", f"/articles/{a['slug']}/", page="", a=a, title=f"{a['title']} | Engr. Peter John R. Bacani",
               description=a["description"], og_image="home", canonical=f"/articles/{a['slug']}/")
    render("404.html"''', 1)
    return s


rw("tools/build.py", bld)

# ---- shared block macros
w("templates/partials/blocks.html", """{% macro fig(id) %}
  {% set r = registry.images[id] %}
  <figure class="fig">
    <a class="fig-open" href="{{ full_url(id) }}" data-caption="{{ r.caption|default(r.alt) }}" aria-label="Enlarge image: {{ r.alt }}">
      {{ img(id, sizes="(min-width: 960px) 704px, 92vw", max_w=1200, alt=r.alt) }}
    </a>
    {% if r.caption %}<figcaption>{{ r.caption }}</figcaption>{% endif %}
  </figure>
{% endmacro %}

{% macro vid(id) %}
  {% set v = manifest.videos[id] %}
  <figure class="fig video">
    <video controls preload="metadata" playsinline width="{{ v.w }}" height="{{ v.h }}" poster="{{ u('/media/img/' ~ v.poster) }}">
      <source src="{{ u('/media/video/' ~ v.file) }}" type="video/mp4">
      Your browser cannot play this video. <a href="{{ u('/media/video/' ~ v.file) }}">Download the MP4</a>.
    </video>
    <figcaption>{{ v.title }} · {{ v.seconds // 60 }}:{{ '%02d'|format(v.seconds % 60) }}</figcaption>
  </figure>
{% endmacro %}

{% macro block(b) %}
  {% if b.type == "p" %}<p>{{ b.text|safe }}</p>
  {% elif b.type == "ul" %}<ul class="prose-list">{% for i in b["items"] %}<li>{{ i|safe }}</li>{% endfor %}</ul>
  {% elif b.type == "table" %}
    <div class="table-wrap" tabindex="0" role="region" aria-label="{{ b.caption }}">
    <table><caption>{{ b.caption }}</caption>
      <thead><tr>{% for h in b.headers %}<th scope="col">{{ h }}</th>{% endfor %}</tr></thead>
      <tbody>{% for r in b.rows %}<tr>{% for c in r %}{% if loop.first %}<th scope="row">{{ c|safe }}</th>{% else %}<td>{{ c|safe }}</td>{% endif %}{% endfor %}</tr>{% endfor %}</tbody>
    </table></div>
  {% elif b.type == "flow" %}
    <figure class="flow">
      <ol>{% for s in b.steps %}<li><span class="step-n">{{ '%02d'|format(loop.index) }}</span><strong>{{ s.label }}</strong>{% if s.detail %}<span>{{ s.detail|safe }}</span>{% endif %}</li>{% endfor %}</ol>
      {% if b.caption %}<figcaption>{{ b.caption }}</figcaption>{% endif %}
    </figure>
  {% elif b.type == "figure" %}{{ fig(b.id) }}
  {% elif b.type == "video" %}{{ vid(b.id) }}
  {% endif %}
{% endmacro %}
""")

w("templates/article.html", """{% extends "base.html" %}
{% from "partials/blocks.html" import block %}
{% block head %}
<script type="application/ld+json">{{ {
  "@context": "https://schema.org", "@type": "Article", "headline": a.title, "description": a.description,
  "author": {"@type": "Person", "name": profile.name}
}|tojson }}</script>
{% endblock %}
{% block main %}
<article class="article">
  <header class="page-head article-head">
    <div class="wrap">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="{{ u('/projects/') }}">Projects</a> / <a href="{{ by_slug[a.project].url }}">{{ by_slug[a.project].name }}</a> / <span aria-current="page">Method article</span></nav>
      <h1>{{ a.title }}</h1>
      <p class="lede">{{ a.lede }}</p>
      <p class="small muted">{{ profile.fullName }} · {{ a.readingTime }}</p>
    </div>
  </header>
  <div class="wrap">
    <div class="prose article-body">
      {% for s in a.sections %}
      <section id="{{ s.id }}" aria-labelledby="{{ s.id }}-h">
        <h2 id="{{ s.id }}-h">{{ s.title }}</h2>
        {% for b in s.blocks %}{{ block(b) }}{% endfor %}
      </section>
      {% endfor %}
      <p class="more"><a class="link-arrow" href="{{ by_slug[a.project].url }}" data-modal>See the full {{ by_slug[a.project].name }} project →</a></p>
    </div>
  </div>
</article>
{% endblock %}
""")

w("templates/role.html", """{% extends "base.html" %}
{% from "partials/card.html" import card %}
{% block main %}
<section class="hero role-hero" aria-labelledby="role-title">
  <div class="wrap role-hero-grid">
    <div>
      <p class="role-kicker">{{ r.nav }}</p>
      <h1 id="role-title">{{ r.headline }}</h1>
      <p class="lede">{{ r.summary }}</p>
      <div class="cta-row">
        <button class="btn btn-primary" type="button" data-resume>View Résumé</button>
        <a class="btn" href="{{ u('/contact/') }}">Contact Me</a>
      </div>
    </div>
    <figure class="portrait role-portrait">{{ img('peter', sizes='(min-width: 960px) 22vw, 50vw', loading='eager', fetchpriority='high') }}</figure>
  </div>
</section>

<section class="section role-why" aria-labelledby="why-h">
  <div class="wrap">
    <h2 id="why-h">Why me for this role</h2>
    <ul class="prose-list role-why-list">{% for w in r.why %}<li>{{ w }}</li>{% endfor %}</ul>
  </div>
</section>

<section class="section role-projects" aria-labelledby="rp-h">
  <div class="wrap">
    <h2 id="rp-h">Most relevant projects</h2>
    <div class="card-grid card-grid-2">
      {% for p in r.project_cards %}
      <div class="role-card-wrap">
        {{ card(p) }}
        <p class="role-why-line"><strong>Relevance</strong> {{ p.why }}</p>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<section class="section role-skills" aria-labelledby="rs-h">
  <div class="wrap">
    <h2 id="rs-h">Core tools</h2>
    <ul class="chips big">{% for t in r.tools %}<li>{{ t }}</li>{% endfor %}</ul>
    <p class="more">{% for s in r.sections %}<a class="link-arrow" href="{{ u('/skills/') }}#{{ s.id }}">{{ s.title }} →</a>{% if not loop.last %} &nbsp; {% endif %}{% endfor %}</p>
  </div>
</section>
{% endblock %}
""")

# ---- skills data + template
sk = json.loads((ROOT / "content/skills.json").read_text(encoding="utf-8"))
sk["glance"] = ["Python", "OpenCV", "scikit-learn", "Flask", "Arduino", "ESP32", "YOLOv11", "SQL"]
for s in sk["sections"]:
    for c in s["capabilities"]:
        if c["title"] == "Technical documentation and communication":
            c["links"] = [
                {"label": "Method article: how RETINA measures vessel complexity", "url": "/articles/retina-vessel-complexity/"},
                {"label": "About and experience", "url": "/about/"},
            ]
(ROOT / "content/skills.json").write_text(json.dumps(sk, indent=2, ensure_ascii=False), encoding="utf-8")
rw("templates/skills.html", lambda s: s.replace("""    <p class="legend small muted">{{ skills.legend }}</p>""", """    <div class="glance">
      <h2 class="glance-title">Skills at a glance</h2>
      <ul class="chips big">{% for g in skills.glance %}<li>{{ g }}</li>{% endfor %}</ul>
    </div>
    <p class="legend small muted">{{ skills.legend }}</p>""", 1))

# ---- RETINA page link to the article
rj = json.loads((ROOT / "content/projects/retina.json").read_text(encoding="utf-8"))
rj["related"] = [{"label": "Method article: how RETINA measures vessel complexity", "url": "/articles/retina-vessel-complexity/"}]
(ROOT / "content/projects/retina.json").write_text(json.dumps(rj, indent=2, ensure_ascii=False), encoding="utf-8")
rw("templates/project.html", lambda s: s.replace("""PDF · {{ d.size }}</span></li>{% endfor %}""", """PDF · {{ d.size }}</span></li>{% endfor %}
          {% for rl in p.related %}<li><a href="{{ u(rl.url) }}">{{ rl.label }}</a></li>{% endfor %}""", 1))

# ---- home: explore by role
rw("templates/home.html", lambda s: s.replace("""All {{ projects|length }} projects →</a></p>
  </div>
</section>""", """All {{ projects|length }} projects →</a></p>
  </div>
</section>

<section class="section role-links" aria-labelledby="roles-h">
  <div class="wrap">
    <header class="section-head"><h2 id="roles-h">Explore by role</h2></header>
    <ul class="role-grid">
      {% for r in roles %}<li><a class="role-link" href="{{ r.url }}"><strong>{{ r.nav }}</strong><span>{{ r.blurb }}</span><span class="role-go" aria-hidden="true">View →</span></a></li>{% endfor %}
    </ul>
    {% for a in articles %}<p class="more">Read: <a class="link-arrow" href="{{ a.url }}">{{ a.title }} →</a></p>{% endfor %}
  </div>
</section>""", 1))

# ---- CSS
c = (ROOT / "static/css/style.css").read_text(encoding="utf-8")
if "role-link" not in c:
    c = c.replace("/* Project modal */", """/* Role pages, article, skills glance */
.glance { margin-top: var(--s-3); padding: var(--s-3); background: var(--accent-soft); border-radius: var(--radius); max-width: 52rem; }
.glance-title { font-size: 0.8rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--accent-strong); margin-bottom: 0.7rem; font-weight: 600; }
.glance .chips li { background: #fff; color: var(--ink); font-weight: 600; }
.role-grid { list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr)); gap: var(--s-2); }
.role-link { display: flex; flex-direction: column; gap: 0.4rem; height: 100%; padding: var(--s-3); border: 1px solid var(--line); border-radius: var(--radius); text-decoration: none; color: var(--ink); transition: border-color var(--ease), box-shadow var(--ease); }
.role-link:hover { border-color: var(--line-strong); box-shadow: 0 6px 22px rgba(16, 19, 22, 0.08); }
.role-link strong { font-size: 1.05rem; }
.role-link span { font-size: 0.92rem; color: var(--muted); }
.role-link .role-go { margin-top: auto; padding-top: 0.4rem; font-weight: 600; color: var(--accent-strong); }
.role-hero { min-height: 0; padding-block: var(--s-5); display: block; }
.role-hero-grid { display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 0.7fr); gap: var(--s-4); align-items: center; }
.role-hero h1 { font-size: var(--step-3); max-width: 24ch; }
.role-kicker { color: var(--accent-light); font-weight: 600; font-size: 0.85rem; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: var(--s-1); }
.role-hero .lede { max-width: 40rem; color: var(--on-dark-muted); font-size: var(--step-1); }
.role-portrait { width: min(100%, 15rem); justify-self: end; }
@media (max-width: 800px) { .role-hero-grid { grid-template-columns: 1fr; } .role-portrait { justify-self: start; width: 9rem; order: -1; } }
.role-why-list { max-width: 46rem; gap: 0.8rem; }
.role-why-line { margin: 0.6rem 0 0; font-size: 0.9rem; color: var(--ink-2); }
.role-why-line strong { font-size: 0.72rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin-right: 0.4rem; }
.article-head h1 { font-size: var(--step-3); max-width: 26ch; }
.article-body { max-width: 42rem; padding-bottom: var(--s-5); }
.article-body section { margin-bottom: var(--s-4); }

/* Project modal */""", 1)
    (ROOT / "static/css/style.css").write_text(c, encoding="utf-8", newline="\n")
print("roles, article and glance wired in")
