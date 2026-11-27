"""The Member Hub section pages (MW 2026-11-25: every Home section opens a real page).

What must hold: each page built from the prototypes opens for a signed-in member, in the app's Hub
header with Page feedback, marked as sample content; signed-out visitors go to sign in; nothing on Home
or on these pages points at a prototype .html file; Home has no placeholder links left; and the 2027 Site
Visit page sends RSVPs to the app's real form.
"""

import re

import pytest
from django.core.management import call_command
from django.test import override_settings
from django.urls import reverse

from apps.accounts.models import User
from apps.portal.hub_pages import PAGES, REAL_PAGES, url_name

ON = {"UI_PROTOTYPE": True, "UI_PROTOTYPE_ONLY": True}


@pytest.fixture
def member(client, db):
    call_command("seed", "--fictional", verbosity=0)
    u = User.objects.get(username="okafor")
    client.force_login(u)
    return u


def test_there_is_a_page_for_every_prototype_section():
    for key in ("research", "story", "community", "threads", "events", "neurosync", "sitevisit"):
        assert key in PAGES
    for key in ("sitevisit-2026", "mentor", "mentee", "core-bn", "core-cn", "core-ni"):
        assert key in PAGES
    assert sum(k.startswith("member-") for k in PAGES) >= 10
    assert sum(k.startswith("thread-") for k in PAGES) >= 10


@override_settings(**ON)
def test_every_page_opens_in_the_hub_design(client, member):
    for key in PAGES:
        r = client.get(reverse(f"portal:{url_name(key)}"))
        assert r.status_code == 200, key
        html = r.content.decode()
        assert 'class="nav hn-app"' in html, key  # the app's header, not the prototype's
        assert member.person.full_name in html, key  # the account menu
        assert 'class="fbk-open"' in html, key  # Page feedback
        assert ('class="sample-note"' in html) == (key not in REAL_PAGES), key
        assert "hub/system.css" in html, key  # the shared design layer (MW 2026-11-25)
        assert "hubchrome.js" not in html and "{%" not in html and "{{" not in html, key
        assert not re.search(r'(?:href|src)="[a-z0-9-]+\.html', html), key
        assert not re.search(r'(?:href|src)="img/', html), key


def test_pages_need_sign_in(client, db):
    r = client.get(reverse("portal:hub_community"))
    assert r.status_code == 302 and "login" in r.url


@override_settings(**ON)
def test_home_has_no_placeholder_links_and_every_link_opens(client, member):
    html = client.get("/").content.decode()
    assert 'href="#"' not in html
    assert not re.search(r'href="[a-z0-9-]+\.html', html)
    local = {h.split("#")[0] for h in re.findall(r'href="(/[^"]*)"', html)}
    local -= {"/accounts/logout/"}
    for href in sorted(local):
        if href.startswith(("/static/", "/hub/count")):
            continue
        assert client.get(href).status_code == 200, href


@override_settings(**ON)
def test_home_section_titles_open_their_pages(client, member):
    html = client.get("/").content.decode()
    for name in (
        "hub_research",
        "hub_events",
        "hub_community",
        "hub_neurosync",
        "hub_sitevisit_2026",
    ):
        assert f'class="sh-link" href="{reverse("portal:" + name)}"' in html, name
    for name in ("hub_mentor", "hub_mentee", "hub_core_bn", "hub_core_cn", "hub_core_ni"):
        assert f'href="{reverse("portal:" + name)}"' in html, name


@override_settings(**ON)
def test_header_opens_research_events_and_community(client, member):
    html = client.get(reverse("portal:hub_events")).content.decode()
    nav = re.search(r'<nav class="nav hn-app".*?</nav>', html, re.S).group(0)
    assert f'href="{reverse("portal:hub_research")}"' in nav
    assert f'href="{reverse("portal:hub_community")}"' in nav
    assert f'href="{reverse("portal:hub_events")}" aria-current="page"' in nav


@override_settings(**ON)
def test_site_visit_rsvp_goes_to_the_real_form(client, member):
    html = client.get(reverse("portal:hub_sitevisit")).content.decode()
    assert f'href="{reverse("portal:sitevisit_rsvp")}"' in html
    assert '<div class="sv-rs" hidden' in html  # the prototype's form never shows
    assert "This form does not send anything yet" not in html


@override_settings(**ON)
def test_home_and_funding_load_the_design_layer(client, member):
    """MW 2026-11-25: one design layer, loaded last, decides the shared pieces on every Hub page."""
    for url in ("/", reverse("portal:funding"), reverse("portal:funding_resources")):
        html = client.get(url).content.decode()
        assert html.index("hub/system.css") > html.index("hub/hub.css"), url


@override_settings(**ON)
def test_joshua_carr_profile_is_real_and_listed(client, member):
    page = client.get(reverse("portal:hub_member_jc")).content.decode()
    assert "Dr. Joshua Carr" in page and "Mitigating Neural Hypoexcitability" in page
    assert "January 26, 2026 to January 25, 2027" in page
    assert 'href="mailto:joshuacarr@k-state.edu"' in page
    directory = client.get(reverse("portal:hub_community")).content.decode()
    assert reverse("portal:hub_member_jc") in directory


@override_settings(**ON)
def test_bethany_plakke_profile_is_real_and_listed(client, member):
    page = client.get(reverse("portal:hub_member_pl")).content.decode()
    assert "Dr. Bethany Plakke" in page and "Fmr1 knockout rats" in page
    assert 'href="mailto:bplakke@ksu.edu"' in page and "Sample content" not in page
    directory = client.get(reverse("portal:hub_community")).content.decode()
    assert reverse("portal:hub_member_pl") in directory


@override_settings(**ON)
def test_julio_hernandez_pavon_profile_is_real_and_listed(client, member):
    page = client.get(reverse("portal:hub_member_hp")).content.decode()
    assert "Dr. Julio Hernandez-Pavon" in page and "neuronal communication" in page
    assert 'href="mailto:juliohpavon@ksu.edu"' in page and "Sample content" not in page
    directory = client.get(reverse("portal:hub_community")).content.decode()
    assert reverse("portal:hub_member_hp") in directory
