"""Requests to join the Member Hub (MW 2026-11-24, approved feature)."""

from django.core import mail

from apps.accounts.models import AccessRequest, ApplicationRole
from apps.people.models import Person, PersonEmail

from .conftest import make_person, make_user

FORM = {
    "first_name": "Rowan",
    "last_name": "Fictional",
    "email": "rowan.fictional@example.edu",
    "department": "Psychological Sciences",
    "connection": "Graduate student in a pilot lab",
    "note": "",
    "website": "",
}


def _admin(reference):
    return make_user(
        make_person("Avery", "Admin"),
        role=reference["roles"][ApplicationRole.Code.ADMINISTRATOR],
    )


def test_sign_in_page_links_to_request_access(client, reference):
    assert "/accounts/request-access/" in client.get("/accounts/login/").content.decode()


def test_request_is_recorded_and_staff_are_told(client, reference, settings):
    settings.EVALUATOR_EMAIL = "office@example.edu"
    r = client.post("/accounts/request-access/", FORM)
    assert r.status_code == 200
    assert "Your request is with the CNAP team" in r.content.decode()
    req = AccessRequest.objects.get()
    assert req.status == AccessRequest.Status.PENDING and req.email == "rowan.fictional@example.edu"
    assert not Person.objects.filter(last_name="Fictional").exists()  # nothing made before approval
    assert mail.outbox and mail.outbox[-1].to == ["office@example.edu"]
    client.post("/accounts/request-access/", FORM)  # the same address again: no duplicate
    assert AccessRequest.objects.count() == 1


def test_bots_and_existing_members_make_no_request(client, reference):
    client.post("/accounts/request-access/", {**FORM, "website": "spam.example"})
    make_person("Kim", "Member", email="kim.member@example.edu")
    r = client.post("/accounts/request-access/", {**FORM, "email": "kim.member@example.edu"})
    assert "Your request is with the CNAP team" in r.content.decode()  # same reply either way
    assert AccessRequest.objects.count() == 0


def test_approve_makes_the_person_and_sends_a_welcome_link(client, reference):
    client.post("/accounts/request-access/", FORM)
    req = AccessRequest.objects.get()
    admin = _admin(reference)
    client.force_login(admin)
    page = client.get("/manage/access-requests/").content.decode()
    assert "Rowan Fictional" in page and "Approve" in page
    mail.outbox.clear()
    r = client.post(f"/manage/access-requests/{req.pk}/decide/", {"decision": "approve"})
    req.refresh_from_db()
    assert req.status == AccessRequest.Status.APPROVED and req.decided_by == admin
    assert PersonEmail.objects.filter(
        email="rowan.fictional@example.edu", person=req.person
    ).exists()
    assert r.status_code == 302 and r.url == f"/manage/people/{req.person.pk}/"
    assert any("Welcome to the CNAP Member Hub" in m.subject for m in mail.outbox)


def test_decline_sends_nothing_and_members_cannot_decide(client, reference):
    client.post("/accounts/request-access/", FORM)
    req = AccessRequest.objects.get()
    member = make_user(make_person("Pat", "Member"))
    client.force_login(member)
    assert (
        client.post(
            f"/manage/access-requests/{req.pk}/decide/", {"decision": "approve"}
        ).status_code
        == 403
    )
    client.force_login(_admin(reference))
    mail.outbox.clear()
    client.post(f"/manage/access-requests/{req.pk}/decide/", {"decision": "decline"})
    req.refresh_from_db()
    assert req.status == AccessRequest.Status.DECLINED and not mail.outbox
    assert not Person.objects.filter(last_name="Fictional").exists()
