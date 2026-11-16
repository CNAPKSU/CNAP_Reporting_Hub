"""The Site Visit RSVP (MW 2026-11-15, approved build). Fictional people only."""

import pytest
from django.core import mail
from django.core.management import call_command
from django.test import override_settings

from apps.accounts.models import User
from apps.audit.models import AuditLog
from apps.outcomes.models import SiteVisitRSVP


@pytest.fixture
def center(db):
    call_command("seed", "--fictional", verbosity=0)


def _login(client, u):
    user = User.objects.get(username=u)
    client.force_login(user)
    return user


BASE = {
    "attend": "person",
    "parts": ["tue-am", "tue-eve"],
    "meals": ["lunch", "dinner"],
    "diet": "Vegetarian",
    "photo_ok": "yes",
    "parking": "drive",
    "hotel_nights": ["mon"],
    "poster": "yes",
    "poster_title": "A fictional poster",
    "poster_abstract": "Short abstract.",
    "connection": "Pilot project leader",
}


@override_settings(UI_PROTOTYPE=True, UI_PROTOTYPE_ONLY=True)
def test_member_rsvps_gets_email_and_can_change_it(center, client):
    u = _login(client, "okafor")
    assert client.get("/site-visit/rsvp/").status_code == 200
    r = client.post("/site-visit/rsvp/", BASE)
    assert r.status_code == 302
    rsvp = SiteVisitRSVP.objects.get(person=u.person, year=2027)
    assert rsvp.meals == ["lunch", "dinner"] and rsvp.photo_ok is True and rsvp.parking is True
    assert rsvp.hotel_nights == ["mon"] and rsvp.poster == "yes" and rsvp.poster_title == "A fictional poster"
    assert len(mail.outbox) == 1 and "Vegetarian" in mail.outbox[0].body
    assert AuditLog.objects.filter(action=AuditLog.Action.CREATE, entity_id=rsvp.pk).exists()
    # change to Zoom: in-person answers are cleared, and there is still one RSVP
    client.post("/site-visit/rsvp/", BASE | {"attend": "zoom"})
    rsvp.refresh_from_db()
    assert SiteVisitRSVP.objects.filter(person=u.person).count() == 1
    assert rsvp.attend == "zoom" and rsvp.meals == [] and rsvp.hotel_nights == [] and rsvp.photo_ok is None
    page = client.get("/site-visit/rsvp/").content.decode()
    assert "You RSVPed" in page and "Save my changes" in page


@override_settings(UI_PROTOTYPE=True, UI_PROTOTYPE_ONLY=True)
def test_long_abstract_and_missing_attendance_are_refused(center, client):
    u = _login(client, "okafor")
    page = client.post("/site-visit/rsvp/", BASE | {"poster_abstract": "word " * 151}).content.decode()
    assert "Please shorten the abstract" in page
    page = client.post("/site-visit/rsvp/", {k: v for k, v in BASE.items() if k != "attend"}).content.decode()
    assert "Please choose how you will attend" in page
    assert not SiteVisitRSVP.objects.filter(person=u.person).exists()


def test_only_administrators_see_the_rsvp_list(center, client):
    _login(client, "okafor")
    assert client.get("/site-visit/rsvps/").status_code == 403
    client.logout()
    _login(client, "mwills")
    assert client.get("/site-visit/rsvps/").status_code == 200
    csv = client.get("/site-visit/rsvps/?format=csv")
    assert csv.status_code == 200 and csv["Content-Type"] == "text/csv"
