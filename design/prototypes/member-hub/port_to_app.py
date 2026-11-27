"""Turn the Member Hub section prototypes into app pages (MW 2026-11-25: make every Home section live).

Run from the repository root:  python3 design/prototypes/member-hub/port_to_app.py

For each prototype page this writes templates/hub/pages/<key>.html. Each page:
  - uses the app's Hub header (hub/_header.html) and Page feedback (_feedback.html) in place of the
    prototype's header and hubchrome.js;
  - links to the app's routes in place of the prototype's .html files (apps/portal/hub_pages.py lists them);
  - loads its styles, scripts, images, and files from static/hub/: the app's hub.css first, for the header,
    then the prototype's guide.css, so the page content looks as approved;
  - carries the "Sample content" note while its people, posts, and dates are the prototype's samples.

It also copies the shared assets into static/hub/. The prototype files themselves are not changed.
"""

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = Path(__file__).resolve().parent
OUT = ROOT / "templates" / "hub" / "pages"
STATIC = ROOT / "static" / "hub"

# Prototype file -> (page key, header section). Keys must match apps/portal/hub_pages.PAGES.
PAGES = {
    "research.html": ("research", "research"),
    "story.html": ("story", "research"),
    "community.html": ("community", "community"),
    "threads.html": ("threads", "community"),
    "thread.html": ("thread", "community"),
    "events.html": ("events", "events"),
    "core-bn.html": ("core-bn", "resources"),
    "core-cn.html": ("core-cn", "resources"),
    "core-ni.html": ("core-ni", "resources"),
    "sitevisit.html": ("sitevisit", "events"),
    "sitevisit-2026.html": ("sitevisit-2026", "events"),
    "mentor.html": ("mentor", "resources"),
    "mentee.html": ("mentee", "resources"),
    "mentee-profile.html": ("mentee-profile", "resources"),
    "neurosync.html": ("neurosync", "events"),
}
for p in sorted(SRC.glob("thread-*.html")):
    PAGES[p.name] = (p.stem, "community")
for p in sorted(SRC.glob("member-*.html")):
    PAGES[p.name] = (p.stem, "community")

# Prototype pages that already exist in the app under another name.
APP_ROUTES = {
    "index.html": "home",
    "reporting.html": "portal:tasks",
    "reporting-history.html": "portal:history",
    "funding.html": "portal:funding",
    "funding-resources.html": "portal:funding_resources",
    "funding-news.html": "portal:funding_news",
}

FILES = {"cnap-mentor-meeting-log.xlsx", "neurosync-flyer.pdf"}

SAMPLE_NOTE = (
    '<div class="wrap hp-sample"><p class="sample-note">Sample content. '
    "The people, posts, and dates on this page are examples until it is connected to the Hub.</p></div>"
)


def url_name(key):
    return "portal:hub_" + key.replace("-", "_")


def link(href):
    """Prototype href -> template expression, or None to leave it as it is."""
    m = re.fullmatch(r"([a-z0-9-]+\.html)(#[^\"]*)?", href)
    if not m:
        return None
    page, frag = m.group(1), m.group(2) or ""
    if page in APP_ROUTES:
        return "{% url '" + APP_ROUTES[page] + "' %}" + frag
    if page in PAGES:
        return "{% url '" + url_name(PAGES[page][0]) + "' %}" + frag
    if page == "system.html":
        return "{% url 'home' %}"  # the design foundations stay a prototype
    raise SystemExit(f"No route for {page}")


def asset(path):
    """Prototype asset path -> {% static %} expression, or None."""
    if path.startswith("img/"):
        return "{% static 'hub/" + path + "' %}"
    if path in FILES:
        return "{% static 'hub/files/" + path + "' %}"
    if path in {"guide.js", "meeting-log.js"}:
        return "{% static 'hub/" + path + "' %}"
    return None


FOOT_NAME = "<span>Cognitive and Neurobiological Approaches to Plasticity Center, Kansas State University</span>"
FOOT_LINK = (
    '<a class="ft-site" href="https://www.k-state.edu/cnap/" title="Opens the CNAP website.">'
    "Cognitive and Neurobiological Approaches to Plasticity Center, Kansas State University</a>"
)


def page_fixes(name, body):
    """The few changes a page needs because the app already does the real thing."""
    # The footer's Center name opens the public CNAP website (MW 2026-11-25).
    body = body.replace(FOOT_NAME, FOOT_LINK)
    if name == "sitevisit.html":
        # The app has the real RSVP form (portal:sitevisit_rsvp). The prototype's form stays in the page,
        # hidden, only because the page's script expects its fields; members see a link to the real one.
        body = body.replace(
            '<div class="sv-rs">',
            '<p class="sv-real"><a class="btn pri" href="{% url \'portal:sitevisit_rsvp\' %}">'
            "RSVP for the 2027 Site Visit</a></p>"
            '<div class="sv-rs" hidden aria-hidden="true">',
            1,
        )
        body = body.replace('<p class="proto-note">Prototype. This form does not send anything yet.</p>', "", 1)
    return body


def convert(name, key, active):
    s = (SRC / name).read_text()
    if re.search(r"\{[{%#]", s):
        raise SystemExit(f"{name} contains Django template syntax; escape it first")
    title = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
    title = title.replace("CNAP Member Hub", "{{ platform_name }}")
    body_tag = re.search(r"<body[^>]*>", s).group(0)
    body = s[s.index(body_tag) + len(body_tag) : s.rindex("</body>")]
    # The prototype header and its skip link make way for the app's.
    body = re.sub(r'\s*<a class="skip"[^>]*>.*?</a>', "", body, count=1, flags=re.S)
    body, n = re.subn(r'<header class="hdr">.*?</header>', "", body, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"{name}: no prototype header")
    body = re.sub(r'\s*<script src="hubchrome\.js"[^>]*></script>', "", body)
    extra_css = ""
    if 'href="evcal.css"' in s:
        extra_css = "\n<link rel=\"stylesheet\" href=\"{% static 'hub/evcal.css' %}\">"

    def fix_href(m):
        new = link(m.group(2))
        return m.group(0) if new is None else f'{m.group(1)}"{new}"'

    def fix_asset(m):
        new = asset(m.group(2))
        return m.group(0) if new is None else f'{m.group(1)}"{new}"'

    body = re.sub(r'(href=)"([^"]+)"', fix_href, body)
    body = re.sub(r'((?:src|href|data-dl)=)"([^"]+)"', fix_asset, body)
    body = re.sub(r'(srcset=)"([^"]+)"', lambda m: m.group(0), body)
    if re.search(r'(?:src|href)="(?:img/|[a-z0-9-]+\.(?:html|js|css|xlsx|pdf)["#])', body):
        left = re.findall(r'(?:src|href)="((?:img/|[a-z0-9-]+\.(?:html|js|css|xlsx|pdf))[^"]*)"', body)
        raise SystemExit(f"{name}: unconverted paths {left[:5]}")
    body = page_fixes(name, body)
    body, n = re.subn(r'(<main id="main"[^>]*>)', r"\1\n" + SAMPLE_NOTE, body, count=1)
    if n != 1:
        raise SystemExit(f"{name}: no <main id=main>")
    body_tag = body_tag.replace("<body", '<body data-hub-page="' + key + '"', 1)
    return f"""{{% load static %}}<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<link rel="icon" type="image/png" sizes="32x32" href="{{% static 'img/favicon-32.png' %}}">
<link rel="apple-touch-icon" href="{{% static 'img/apple-touch-icon.png' %}}">
<link rel="stylesheet" href="{{% static 'hub/hub.css' %}}">
<link rel="stylesheet" href="{{% static 'hub/guide.css' %}}">{extra_css}
<link rel="stylesheet" href="{{% static 'hub/system.css' %}}">
</head>
{body_tag}
{{# Built by design/prototypes/member-hub/port_to_app.py from {name}. Change the prototype and run it again. #}}
{{% if demo_site %}}<div class="demo-note" role="note">Test copy with fictional data only.</div>{{% endif %}}
<a class="skip" href="#main">Skip to main content</a>
{{% include "hub/_header.html" with active="{active}" %}}
{body.strip()}
{{% include "_feedback.html" %}}
<script src="{{% static 'hub/page.js' %}}" defer></script>
<script src="{{% static 'js/dropclose.js' %}}" defer></script>
</body>
</html>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (key, active) in PAGES.items():
        (OUT / f"{key}.html").write_text(convert(name, key, active))
    for f in ("guide.css", "evcal.css", "guide.js", "meeting-log.js"):
        shutil.copyfile(SRC / f, STATIC / f)
    for f in (SRC / "img").iterdir():
        shutil.copyfile(f, STATIC / "img" / f.name)
    (STATIC / "files").mkdir(exist_ok=True)
    for f in FILES:
        shutil.copyfile(SRC / f, STATIC / "files" / f)
    print(f"{len(PAGES)} pages written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
