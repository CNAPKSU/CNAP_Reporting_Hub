"""The CNAP calendar: a live subscribe feed, the Calendar admin page, and events by email (MW 2026-11-27)."""

import json
from datetime import date, time, timedelta

import pytest
from django.core import mail
from django.utils import timezone

from apps.accounts import access
from apps.accounts.models import User
from apps.events import feed, inbound
from apps.events.models import CenterEvent
from apps.people.models import PersonEmail
from apps.reporting.models import SpeakerTalk
from tests.test_nih_documents import center  # noqa: F401  (fixture)

pytestmark = pytest.mark.django_db


def _manager(client=None):
    u = next(u for u in User.objects.all() if access.can_manage(u))
    if client:
        client.force_login(u)
    return u


def _url(key=None):
    return f"/calendar/{key or feed.feed_key()}.ics"


def test_feed_has_published_events_talks_and_due_dates_but_no_drafts(client, center):
    u = _manager()
    soon = timezone.localdate() + timedelta(days=10)
    CenterEvent.objects.create(
        title="Spring retreat", day=soon, starts=time(9), ends=time(15), created_by=u
    )
    CenterEvent.objects.create(title="Secret draft", day=soon, status="draft", created_by=u)
    CenterEvent.objects.create(title="Called off", day=soon, status="cancelled", created_by=u)
    SpeakerTalk.objects.create(
        speaker=u.person,
        title="Sleep and memory",
        ends_at=timezone.now() + timedelta(days=3),
        created_by=u,
    )
    r = client.get(_url())
    assert r.status_code == 200 and r["Content-Type"].startswith("text/calendar")
    body = r.content.decode()
    assert body.startswith("BEGIN:VCALENDAR") and body.rstrip().endswith("END:VCALENDAR")
    assert "Spring retreat" in body and "Sleep and memory" in body
    assert "CNAP reporting due" in body
    assert "Secret draft" not in body and "Called off" not in body
    assert all(len(line.encode()) <= 75 for line in body.split("\r\n"))
    # a wrong key gets nothing
    assert client.get(_url("nope")).status_code == 404


def test_the_same_event_keeps_its_uid_and_a_change_raises_its_sequence(client, center):
    u = _manager()
    e = CenterEvent.objects.create(
        title="Retreat", day=timezone.localdate() + timedelta(days=5), created_by=u
    )
    first = client.get(_url()).content.decode()
    assert f"UID:{e.uid}" in first.replace("\r\n ", "")
    e.title = "Retreat (new room)"
    e.save()
    second = client.get(_url()).content.decode().replace("\r\n ", "")
    assert f"UID:{e.uid}" in second and "Retreat (new room)" in second


def test_home_and_events_show_the_sync_box(client, center):
    _manager(client)
    for path in ("/", "/events/"):
        html = client.get(path).content.decode()
        assert "Sync the CNAP calendar" in html, path
        assert "outlook.office.com/calendar/0/addfromweb" in html
        assert "calendar.google.com/calendar/r?cid=" in html
        assert "webcal://" in html


def test_calendar_page_add_draft_publish_cancel(client, center):
    _manager(client)
    assert "Add an event" in client.get("/manage/calendar/").content.decode()
    day = (timezone.localdate() + timedelta(days=20)).isoformat()
    r = client.post("/manage/calendar/save/", {"title": "Poster day", "day": day, "go": "draft"})
    assert r.status_code == 302
    e = CenterEvent.objects.get(title="Poster day")
    assert e.status == "draft"
    assert "Poster day" not in client.get(_url()).content.decode()
    client.post(f"/manage/calendar/{e.pk}/status/", {"act": "publish"})
    e.refresh_from_db()
    assert e.status == "published" and "Poster day" in client.get(_url()).content.decode()
    client.post(f"/manage/calendar/{e.pk}/status/", {"act": "cancel"})
    e.refresh_from_db()
    assert e.status == "cancelled" and "Poster day" not in client.get(_url()).content.decode()
    # an end time with no start is refused
    client.post(
        "/manage/calendar/save/", {"title": "Bad", "day": day, "ends": "10:00", "go": "publish"}
    )
    assert not CenterEvent.objects.filter(title="Bad").exists()


def _postmark(sender, subject, body):
    return json.dumps(
        {"From": sender, "FromFull": {"Email": sender}, "Subject": subject, "TextBody": body}
    )


def test_an_emailed_event_from_a_manager_becomes_a_draft(client, center):
    u = _manager()
    addr = PersonEmail.objects.filter(person=u.person).first()
    if addr is None:
        addr = PersonEmail.objects.create(
            person=u.person, email="evaluator@example.org", is_primary=True
        )
    mail.outbox.clear()
    r = client.post(
        f"/calendar/inbound/{feed.inbound_key()}/",
        _postmark(
            addr.email,
            "Event: Spring retreat",
            "Date: April 10, 2027\nTime: 9 a.m. to 3 p.m.\nWhere: Alumni Center\n",
        ),
        content_type="application/json",
    )
    assert r.status_code == 200
    e = CenterEvent.objects.get(title="Spring retreat")
    assert e.status == "draft" and e.source == "email"
    assert e.day == date(2027, 4, 10) and e.starts == time(9) and e.ends == time(15)
    assert e.place == "Alumni Center"
    assert (
        mail.outbox
        and mail.outbox[-1].to == [addr.email]
        and "/manage/calendar/" in mail.outbox[-1].body
    )


def test_an_emailed_event_from_anyone_else_is_ignored(client, center):
    r = client.post(
        f"/calendar/inbound/{feed.inbound_key()}/",
        _postmark("stranger@example.com", "Party", "Date: May 1, 2027"),
        content_type="application/json",
    )
    assert r.status_code == 200 and not CenterEvent.objects.exists()
    bad = client.post("/calendar/inbound/wrong/", "{}", content_type="application/json")
    assert bad.status_code == 404


def test_parse_reads_ranges_noon_and_missing_dates():
    today = date(2026, 11, 27)
    d = inbound.parse(
        "Fwd: Lab meeting", "When: Dec 3, noon to 1:30 pm\nhttps://k-state.edu/x", today
    )
    assert d["title"] == "Lab meeting" and d["day"] == date(2026, 12, 3)
    assert d["starts"] == time(12) and d["ends"] == time(13, 30)
    assert d["url"] == "https://k-state.edu/x"
    d = inbound.parse("Retreat", "March 3-5, 2027", today)
    assert d["day"] == date(2027, 3, 3) and d["end_day"] == date(2027, 3, 5)
    d = inbound.parse("Someday", "We should meet.", today)
    assert d["check_date"] is True
