import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "templates" / "skills.html"
s = p.read_text(encoding="utf-8")

# 1. remove the strip from the top of the page
s = re.sub(r'\n<section class="wrap tech-stack".*?</section>\n', "\n", s, flags=re.S)

# 2. add G to the side panel
s = s.replace('''{% endfor %}
    </ul>
  </nav>''', '''{% endfor %}
      <li><a href="#stack"><span class="letter">G</span>Tech stack</a></li>
    </ul>
  </nav>''', 1)

# 3. add section G after the capability sections
stack = '''  <section class="skill-section" id="stack" aria-labelledby="stack-h">
    <header class="skill-section-head">
      <span class="section-letter" aria-hidden="true">G</span>
      <div>
        <h2 id="stack-h">{{ techstack.title }}</h2>
        <p class="section-summary">Languages, frameworks, databases, data tools and design software.</p>
      </div>
    </header>
    <ul class="stack">
      {% for t in techstack["items"] %}
      <li class="badge{% if t.color|lower == '#ffffff' %} badge-light{% endif %}" style="--bg: {{ t.color }}; --fg: {{ t.fg }}">
        {% if t.path %}<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="{{ t.path }}"/></svg>{% endif %}<span>{{ t.name }}</span>
      </li>
      {% endfor %}
    </ul>
  </section>
'''
s = s.replace("  {% endfor %}\n  </div>\n</div>\n{% endblock %}", "  {% endfor %}\n" + stack + "  </div>\n</div>\n{% endblock %}", 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("stack" in s, s.count("tech-stack"))
