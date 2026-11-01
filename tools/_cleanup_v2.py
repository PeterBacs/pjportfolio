"""One-off redesign cleanup (kept for reference; safe to delete)."""
import json
import re
from pathlib import Path

R = Path(__file__).resolve().parent.parent


def rw(path, fn):
    p = R / path
    s = p.read_text(encoding="utf-8")
    p.write_text(fn(s), encoding="utf-8", newline="\n")


def clean(s):
    s = re.sub(r'\s*<p class="eyebrow mono">.*?</p>', "", s)
    return re.sub(r'<span class="sec-n mono">\d+</span>', "", s)


for t in ("skills", "about", "resume", "contact", "404", "projects"):
    rw(f"templates/{t}.html", clean)

rw("templates/projects.html", lambda s: re.sub(r'\s*<p class="section-lede">One collection.*?</p>', "", s).replace("<h1>All projects</h1>", "<h1>Projects</h1>"))
rw("templates/skills.html", lambda s: re.sub(r'<p class="section-lede">Each skill names.*?</p>', '<p class="lede">Each skill shows where it is documented.</p>', s).replace("<h1>Skills, with the evidence behind them</h1>", "<h1>Technical skills</h1>").replace('<span class="mono">Basis</span>', "Source:"))
rw("templates/about.html", lambda s: s.replace('<p class="intro">{{ b }}</p>', '<p class="lede">{{ b }}</p>').replace('<p class="small muted">Licence numbers appear on the downloadable résumé.</p>', "").replace("<h1>Engineer, educator and research mentor</h1>", "<h1>About</h1>").replace("How this background supports engineering work", "What this background brings").replace("Core competencies (from the résumé)", "Core competencies"))
rw("templates/resume.html", lambda s: re.sub(r'\s*<p class="section-lede">Download the résumé.*?</p>', "", s).replace("<h1>Résumé and project documents</h1>", "<h1>Résumé &amp; Research</h1>").replace('<a class="btn btn-primary" href="{{ resume.url }}" download>', '<a class="btn btn-primary" href="{{ resume.url }}" data-download="{{ resume.file }}">').replace('<p class="small muted">The supplied project documents are short summaries of one paragraph each. The project pages carry the technical detail.</p>', "").replace('<p class="small muted">The RETINA study draft (RetinaMFA) is summarised on its project page; the full draft is available on request.</p>', ""))
rw("templates/contact.html", lambda s: re.sub(r'\s*<p class="section-lede">Email is the most reliable.*?</p>', "", s).replace('<a href="{{ resume.url }}" download>', '<a href="{{ resume.url }}" data-download="{{ resume.file }}">'))
rw("templates/404.html", lambda s: re.sub(r'\s*<p class="section-lede">.*?</p>', "", s))

# ---- profile: shorter copy
p = json.loads((R / "content/profile.json").read_text(encoding="utf-8"))
p["intro"] = ["Registered Electronics Engineer with a Master of Science in Engineering and more than ten years of teaching. My projects cover machine-learning image analysis, wearable safety electronics, sensor-based prototypes and mathematical modelling."]
p["bio"] = [
    "I trained in electronics and computer engineering, then completed graduate degrees in engineering and in mathematics teaching. I started as an engineering instructor at Isabela State University and now teach mathematics and STEM at Lanna National High School, where I also mentor research, robotics and innovation teams.",
    "The projects on this site are prototype and research work, not commercial products.",
]
p["strengths"] = [
    {"title": "Problem solving", "text": "Engineering mathematics and modelling underpin my project work, from fractal analysis to seismic decay models."},
    {"title": "Experimentation", "text": "Prototype building and system testing are part of my teaching and my mentoring of competition teams."},
    {"title": "Collaboration", "text": "Mentoring student teams means scoping work with people at different levels and keeping documentation consistent."},
    {"title": "Technical communication", "text": "Ten years of explaining mathematics and engineering shapes how I write: define the problem, state what was built, show what was demonstrated."},
]
(R / "content/profile.json").write_text(json.dumps(p, indent=2, ensure_ascii=False), encoding="utf-8")

# ---- projects: cleaner status labels
for f in (R / "content/projects").glob("*.json"):
    j = json.loads(f.read_text(encoding="utf-8"))
    if j["status"].startswith("Working software"):
        j["status"] = "Working demo"
        j["statusGroup"] = "Working demo"
    f.write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding="utf-8")

# ---- skills: shorter notes
s = (R / "content/skills.json").read_text(encoding="utf-8")
s = s.replace("Listed as core competencies in the résumé. Specific microcontrollers and communication protocols are not named in the supplied project documents, so none are claimed here.", "Listed as core competencies in the résumé.")
s = s.replace("Listed as a core competency in the résumé, which also records mentoring of robotics and innovation projects. No robotics project is documented on this site yet.", "Listed in the résumé, including mentoring of robotics and innovation projects.")
(R / "content/skills.json").write_text(s, encoding="utf-8")

# ---- JS: reliable file download
js = (R / "static/js/site.js").read_text(encoding="utf-8")
if "data-download" not in js:
    js = js.replace("  // Copy email", """  // Force a real download for links marked data-download (browsers otherwise open PDFs and videos inline)
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-download]");
    if (!a || e.ctrlKey || e.metaKey || e.shiftKey || e.button) return;
    e.preventDefault();
    fetch(a.href).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.blob();
    }).then(function (blob) {
      var url = URL.createObjectURL(blob);
      var t = document.createElement("a");
      t.href = url;
      t.download = a.getAttribute("data-download");
      document.body.appendChild(t);
      t.click();
      t.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
    }).catch(function () { window.location.href = a.href; });
  });

  // Copy email""")
    (R / "static/js/site.js").write_text(js, encoding="utf-8")
print("cleanup done")
