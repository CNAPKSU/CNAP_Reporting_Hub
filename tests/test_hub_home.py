"""The CNAP Member Hub homepage (MW 2026-11-13).

What must hold: with the redesign off, "/" still sends people where it always did. With it on, the
homepage reads the person's own records only, never another member's funding matches; the reporting
numbers match My work; administrators see the Center's progress and members don't; sections the Hub
has no records for say so; and the page writes nothing.
"""

from datetime import timedelta

import pytest
from django.core.management import call_command
from django.db import connection
from django.test import override_settings
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from apps.accounts.models import User
from apps.outcomes.models import FundingMatch, FundingOpportunity
from apps.portal import hub, presenters
from apps.reporting.models import Assignment, ReportingPeriod, SpeakerTalk

PW = "Demo-Password-2026"
ON = {"UI_PROTOTYPE": True, "UI_PROTOTYPE_ONLY": True}


@pytest.fixture
def center(db):
    call_command("seed", "--fictional", verbosity=0)
    return ReportingPeriod.objects.get(status="open")


def _login(client, username):
    assert client.login(username=username, password=PW)
    return User.objects.get(username=username)


def test_off_by_default_home_still_redirects(client, center):
    _login(client, "okafor")
    r = client.get("/")
    assert r.status_code == 302 and r.url.endswith("/tasks/")


@override_settings(UI_PROTOTYPE=True, UI_PROTOTYPE_ONLY=False)
def test_current_design_switch_keeps_the_old_home(client, center):
    _login(client, "okafor")
    s = client.session
    s["ui_view"] = "before"
    s.save()
    r = client.get("/")
    assert r.status_code == 302 and r.url.endswith("/tasks/")


@override_settings(**ON)
def test_member_gets_the_homepage_with_their_own_reporting(client, center):
    u = _login(client, "okafor")
    r = client.get("/")
    assert r.status_code == 200
    assert "hub/home.html" in {t.name for t in r.templates if t.name}
    html = r.content.decode()
    assert f", {u.person.first_name}.</h1>" in html
    mine = list(
        Assignment.objects.filter(person=u.person, reporting_period=center).select_related(
            "form_definition", "form_version", "project", "core", "completion_pathway"
        )
    )
    t = presenters.task_list(u.person, center, mine)
    assert f"{t['done_n']} of {t['total']} submitted" in html
    assert f"{center.name} reporting" in html
    assert 'href="/tasks/"' in html and 'href="/funding/"' in html
    assert "CNAP Member Hub" in html
    assert 'class="fbk-open"' in html  # the page-feedback button reviewers use
    assert 'id="hub-cal"' in html


@override_settings(**ON)
def test_only_the_persons_own_funding_matches_show(client, center):
    okafor = User.objects.get(username="okafor").person
    varga = User.objects.get(username="varga").person
    secret = FundingOpportunity.objects.create(
        name="Fictional award picked only for Varga", source_kind="foundation"
    )
    FundingMatch.objects.create(opportunity=secret, person=varga, why="For Varga alone.")
    mine = FundingOpportunity.objects.create(
        name="Fictional award picked for Okafor",
        source_kind="foundation",
        deadline=timezone.localdate() + timedelta(days=40),
    )
    FundingMatch.objects.create(opportunity=mine, person=okafor, why="Fits the sleep work.")
    _login(client, "okafor")
    html = client.get("/").content.decode()
    assert "Fictional award picked for Okafor" in html
    assert "Fictional award picked only for Varga" not in html


@override_settings(**ON)
def test_administrators_see_center_progress_and_members_do_not(client, center):
    _login(client, "okafor")
    html = client.get("/").content.decode()
    assert "Center reporting" not in html and "/manage/" not in html
    client.logout()
    _login(client, "mwills")
    html = client.get("/").content.decode()
    assert "Center reporting" in html and 'href="/manage/"' in html


@override_settings(**ON)
def test_next_neurosync_talk_comes_from_the_schedule(client, center):
    u = _login(client, "okafor")
    speaker = User.objects.get(username="varga").person
    SpeakerTalk.objects.create(
        speaker=speaker,
        title="A fictional talk on sleep spindles",
        ends_at=timezone.now() + timedelta(days=2),
        auto_send=False,
    )
    html = client.get("/").content.decode()
    assert "A fictional talk on sleep spindles" in html
    assert speaker.full_name in html
    assert u.person.full_name in html  # the account menu


@override_settings(**ON)
def test_sections_without_records_are_marked_as_samples(client, center):
    _login(client, "okafor")
    html = client.get("/").content.decode()
    assert html.count('class="sample-note"') >= 4  # research, toolkit, community, photographs


@override_settings(**ON)
def test_the_homepage_writes_nothing(client, center):
    _login(client, "okafor")
    with CaptureQueriesContext(connection) as q:
        client.get("/")
    writes = [
        x["sql"]
        for x in q.captured_queries
        if x["sql"].lstrip().upper().startswith(("INSERT", "UPDATE", "DELETE"))
        and "django_session" not in x["sql"]
    ]
    assert writes == []


def test_role_lines_are_plain_words(center):
    u = User.objects.get(username="okafor")
    rels = list(u.person.current_relationships().select_related("relationship_type", "core"))
    lines = hub.role_lines(u.person, rels)
    assert lines and not any("(" in x for x in lines)


@override_settings(**ON)
def test_funding_page_uses_the_hub_design_with_the_same_form_and_sections(client, center):
    """Funding and news in the Member Hub design (MW 2026-11-14): same sections, form, and links."""
    _login(client, "okafor")
    r = client.get("/funding/")
    assert r.status_code == 200
    names = {t.name for t in r.templates if t.name}
    assert "hub/funding.html" in names and "proto/portal/funding.html" not in names
    html = r.content.decode()
    # Three pages in the Hub design (MW 2026-11-14): opportunities, grant resources, and funding news.
    for sid in ("s-for", "s-most", "s-letters", "s-suggest"):
        assert f'id="{sid}"' in html
    res = client.get("/funding/resources/").content.decode()
    for sid in ("s-before", "s-consult", "s-toolkit"):
        assert f'id="{sid}"' in res
    news = client.get("/funding/news/").content.decode()
    for sid in ("s-news", "s-events"):
        assert f'id="{sid}"' in news
    assert 'action="/funding/suggest/"' in html
    for field in ('name="name"', 'name="sponsor"', 'name="url"', 'name="deadline_text"', 'name="why"', 'name="for_everyone"'):
        assert field in html
    assert 'aria-current="page">Funding' in html


def test_funding_page_is_unchanged_with_the_switch_off(client, center):
    _login(client, "okafor")
    r = client.get("/funding/")
    assert r.status_code == 200
    assert "proto/portal/funding.html" in {t.name for t in r.templates if t.name}
    # The separate pages exist only in the Hub design; with the switch off they lead back to the one page.
    assert client.get("/funding/news/").url == "/funding/#s-news"
    assert client.get("/funding/resources/").url == "/funding/#s-before"


def test_ribbon_menus_list_only_pages_the_app_has(client, django_user_model):
    """MW 2026-11-15, approved build: the top ribbon. Each menu link resolves to a page that exists."""
    from django.core.management import call_command
    from django.test import override_settings

    call_command("seed", "--fictional", verbosity=0)
    from apps.accounts.models import User

    client.force_login(User.objects.get(username="okafor"))
    with override_settings(UI_PROTOTYPE=True, UI_PROTOTYPE_ONLY=True):
        html = client.get("/").content.decode()
        assert "{# MW" not in html and "approved build: the prototype ribbon" not in html  # template comments never show
        assert 'class="nav hn-app"' in html and 'aria-controls="rb-fund"' in html and 'aria-controls="rb-rep"' in html
        import re

        for href in set(re.findall(r'<div class="rb-p"[^>]*>(.*?)</div>', html, re.S)):
            for u in re.findall(r'href="([^"#]+)"', href):
                assert client.get(u).status_code == 200, u
