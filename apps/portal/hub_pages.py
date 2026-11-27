"""The Member Hub section pages (MW 2026-11-25): Research, Community, Events, the research cores,
the Site Visit, the onboarding guides, and NeuroSync, built from design/prototypes/member-hub/ by
port_to_app.py. Each page is a template in templates/hub/pages/ with the app's Hub header; its content
is the approved prototype's, marked as sample content until it is connected to the Hub's records.
"""

from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path

from . import hub

_TEMPLATES = Path(__file__).resolve().parents[2] / "templates" / "hub" / "pages"

# key -> URL path. The key is the prototype file's name and the template's name.
PAGES = {
    "research": "research/",
    "story": "research/stories/sleep-and-memory/",
    "community": "community/",
    "threads": "community/threads/",
    "thread": "community/threads/eeg-collaborator/",
    "events": "events/",
    "core-bn": "cores/behavioral-neuroscience/",
    "core-cn": "cores/cognitive-neuroscience/",
    "core-ni": "cores/neuroinformatics/",
    "sitevisit": "site-visit/",
    "sitevisit-2026": "site-visit/2026/",
    "mentor": "guides/mentors/",
    "mentee": "guides/project-leaders/",
    "mentee-profile": "guides/project-leaders/profile/",
    "neurosync": "neurosync/",
}
for _p in sorted(_TEMPLATES.glob("thread-*.html")):
    PAGES[_p.stem] = f"community/threads/{_p.stem.removeprefix('thread-')}/"
for _p in sorted(_TEMPLATES.glob("member-*.html")):
    PAGES[_p.stem] = f"community/members/{_p.stem.removeprefix('member-')}/"

# Pages about real people and events, without the "Sample content" note (MW 2026-11-26).
REAL_PAGES = {"member-jc", "member-pl", "member-hp", "sitevisit-2026"}


def url_name(key):
    return "hub_" + key.replace("-", "_")


@login_required
def page(request, key):
    return render(request, f"hub/pages/{key}.html", hub.chrome(request))


urlpatterns = [path(p, page, {"key": k}, name=url_name(k)) for k, p in PAGES.items()]
