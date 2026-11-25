"""Members ask to change their own roles, and a role added mid-session brings its forms (MW 2026-11-24)."""

import pytest
from django.core import mail
from django.urls import reverse
from django.utils import timezone

from apps.common.enums import PeriodStatus
from apps.reporting.models import Assignment, RosterSuggestion
from apps.reporting.services import assignments
from apps.reporting.services import roster_check as rc

from .conftest import make_person, make_user, relate


@pytest.fixture
def evaluator(reference):
    return make_user(
        make_person("Morgan", "Wills"), username="mw", role=reference["roles"]["administrator"]
    )


@pytest.fixture
def member(reference):
    p = make_person("Avery", "Sample")
    relate(p, reference["types"]["cnap_member"])
    return make_user(p, username="avery")


def test_member_asks_from_profile_and_evaluator_is_told(client, member, settings):
    settings.EVALUATOR_EMAIL = "evaluator@k-state.example"
    client.force_login(member)
    page = client.get(reverse("portal:profile")).content.decode()
    assert "Suggest a change to my roles" in page
    r = client.post(
        reverse("portal:profile"),
        {"action": "role_change", "role_note": "I became a core user of the NI Core."},
    )
    assert r.status_code == 302 and r.url.endswith("#roles")
    s = RosterSuggestion.objects.get()
    assert s.kind == RosterSuggestion.Kind.OWN and s.link is None
    assert s.person == member.person and "NI Core" in s.note
    assert mail.outbox and "asks to change their CNAP roles" in mail.outbox[0].subject
    # Nothing on the roster changed.
    assert list(member.person.relationships.values_list("relationship_type__code", flat=True)) == [
        "cnap_member"
    ]


def test_empty_request_is_refused(client, member):
    client.force_login(member)
    client.post(reverse("portal:profile"), {"action": "role_change", "role_note": "  "})
    assert not RosterSuggestion.objects.exists()


def test_evaluator_sees_and_handles_the_request(client, member, evaluator):
    s = rc.suggest_own(member.person, "Please add me as a pilot mentor.")
    client.force_login(evaluator)
    page = client.get(reverse("manage:access_requests")).content.decode()
    assert "Role changes members asked for" in page and "pilot mentor" in page
    client.post(reverse("manage:role_request_decide", args=[s.pk]), {"decision": "done"})
    s.refresh_from_db()
    assert s.status == RosterSuggestion.Status.DONE and s.decided_by == evaluator
    page = client.get(reverse("manage:access_requests")).content.decode()
    assert "No role changes are waiting." in page


def test_roster_check_page_lists_member_requests(client, member, evaluator, period):
    rc.suggest_own(member.person, "I left the BN Core in October.")
    client.force_login(evaluator)
    page = client.get(f"/manage/periods/{period.pk}/roster-check/").content.decode()
    assert "Avery Sample asks to change their roles" in page
    assert "From Avery Sample’s profile" in page


def test_role_added_during_open_session_brings_its_forms(
    client, evaluator, okafor, forms, period, reference, projects
):
    assignments.generate(period)
    before = set(
        Assignment.objects.filter(person=okafor, reporting_period=period).values_list(
            "form_definition__code", "project_id"
        )
    )
    assert ("pilot_mentor_report", projects["C"].pk) not in before
    client.force_login(evaluator)
    r = client.post(
        reverse("manage:relationship_add", args=[okafor.pk]),
        {
            "relationship_type": reference["types"]["pilot_mentor"].pk,
            "project": projects["C"].pk,
            "start": period.opens_at.date().isoformat(),
        },
        follow=True,
    )
    shown = [str(m) for m in r.context["messages"]]
    assert f"Added {reference['types']['pilot_mentor'].name}." in shown, shown
    after = set(
        Assignment.objects.filter(person=okafor, reporting_period=period).values_list(
            "form_definition__code", "project_id"
        )
    )
    assert ("pilot_mentor_report", projects["C"].pk) in after
    assert before <= after  # nothing removed


def test_catch_up_only_touches_open_sessions_and_never_removes(okafor, forms, period):
    assignments.generate(period)
    n = Assignment.objects.filter(person=okafor).count()
    assert assignments.catch_up(okafor) == 0
    period.status, period.closed_at = PeriodStatus.CLOSED, timezone.now()
    period.save()
    assert assignments.catch_up(okafor) == 0
    assert Assignment.objects.filter(person=okafor).count() == n
