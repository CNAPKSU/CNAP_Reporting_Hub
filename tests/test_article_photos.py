"""Article photos on funding news and events (MW 2026-11-15, approved build). A photo shows only after a person
approves the photo. Fictional records only; the article lookup is faked, so no network call is made."""

import pytest
from django.core.management import call_command
from django.test import override_settings

from apps.accounts.models import User
from apps.outcomes import photos
from apps.outcomes.models import FundingEvent, FundingNewsItem


@pytest.fixture
def center(db):
    call_command("seed", "--fictional", verbosity=0)


def _login(client, u):
    client.force_login(User.objects.get(username=u))


def test_parse_preview_reads_og_image_and_makes_it_absolute():
    html = '<head><meta property="og:image" content="/img/lab.jpg"><meta property="og:image:alt" content="A fictional lab"></head>'
    assert photos.parse_preview(html, "https://example.org/news/1") == (
        "https://example.org/img/lab.jpg",
        "A fictional lab",
    )
    assert photos.parse_preview("<head></head>", "https://example.org/") == ("", "")


def test_find_photo_waits_for_approval_then_shows(center, client, monkeypatch):
    n = FundingNewsItem.objects.create(
        headline="A fictional news item", summary="One line.", source_url="https://example.org/a"
    )
    monkeypatch.setattr(
        photos,
        "find_preview",
        lambda url, timeout=6: ("https://example.org/p.jpg", "A fictional photo"),
    )
    _login(client, "mwills")
    client.post(f"/manage/funding/news/{n.pk}/do/", {"action": "find_photo"})
    n.refresh_from_db()
    assert (
        n.photo_url == "https://example.org/p.jpg"
        and n.photo_alt == "A fictional photo"
        and not n.photo_approved
    )
    assert not n.show_photo
    # approve, with the credit
    client.post(
        f"/manage/funding/news/{n.pk}/do/",
        {
            "headline": n.headline,
            "summary": n.summary,
            "source_url": n.source_url,
            "photo_url": n.photo_url,
            "photo_seen": n.photo_url,
            "photo_alt": n.photo_alt,
            "photo_credit": "Fictional University",
            "photo_approved": "1",
        },
    )
    n.refresh_from_db()
    assert n.show_photo and n.photo_credit == "Fictional University"
    # changing the image address without seeing the new image clears the approval
    client.post(
        f"/manage/funding/news/{n.pk}/do/",
        {
            "headline": n.headline,
            "summary": n.summary,
            "source_url": n.source_url,
            "photo_url": "https://example.org/other.jpg",
            "photo_seen": n.photo_url,
            "photo_approved": "1",
        },
    )
    n.refresh_from_db()
    assert not n.photo_approved


@override_settings(UI_PROTOTYPE=True, UI_PROTOTYPE_ONLY=True)
def test_members_see_only_approved_photos(center, client):
    FundingNewsItem.objects.create(
        headline="Approved fictional item",
        summary="One line.",
        photo_url="https://example.org/yes.jpg",
        photo_credit="Fictional credit",
        photo_approved=True,
    )
    FundingNewsItem.objects.create(
        headline="Unapproved fictional item",
        summary="One line.",
        photo_url="https://example.org/no.jpg",
    )
    _login(client, "okafor")
    html = client.get("/funding/news/").content.decode()
    assert "https://example.org/yes.jpg" in html and "Photo: Fictional credit" in html
    assert "https://example.org/no.jpg" not in html


def test_event_photo_fields_save(center, client):
    _login(client, "mwills")
    client.post(
        "/manage/funding/events/new/do/",
        {
            "title": "A fictional talk",
            "starts_on": "2027-01-15",
            "photo_url": "example.org/e.jpg",
            "photo_alt": "A podium",
            "photo_approved": "1",
        },
    )
    e = FundingEvent.objects.get(title="A fictional talk")
    assert e.photo_url == "https://example.org/e.jpg" and e.photo_approved
