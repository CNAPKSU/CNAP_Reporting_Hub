"""My tasks, calmer layout (MW 2026-10-27): progress up top, Opt out explained in its section,
no per-section "1 to do", "What's this?" instead of a triangle, and section progress on started forms."""

import pytest
from django.core.management import call_command

from apps.accounts.models import User
from apps.common.enums import QuestionType
from apps.forms_engine.runtime import FormSchema
from apps.portal.presenters import section_progress
from apps.reporting.models import Assignment, ReportingPeriod
from apps.reporting.services import assignments as asg
from apps.reporting.services import responses as rs

OPTION_TYPES = rs.OPTION_TYPES


@pytest.fixture
def okafor(db):
    call_command("seed", "--fictional", verbosity=0)
    asg.generate(ReportingPeriod.objects.get(status="open"))
    return User.objects.get(username="okafor")


def _value(q):
    if q.question_type in OPTION_TYPES:
        return q.answer_set.options.first().code
    if q.question_type == QuestionType.DATE:
        return "2026-10-01"
    if q.question_type in (QuestionType.NUMBER, QuestionType.CURRENCY):
        return "1"
    return "Sample text"


def _row(html, a):
    """The My tasks row for one assignment."""
    i = html.index(f"/tasks/{a.pk}/")
    return html[html.rindex("<tr", 0, i) : html.index("</tr>", i)]


def test_page_wording(client, okafor):
    client.force_login(okafor)
    html = client.get("/tasks/").content.decode()
    assert "Opt out*" not in html and "footnote" not in html
    assert "in the last reporting session." in html  # said in the section, next to the button
    assert "You have 1 forms here" not in html
    assert "What’s this?" in html and "▸" not in html
    assert "take about" in html or "takes about" in html or "You’ve finished all" in html


def test_section_progress_counts_only_finished_sections(okafor):
    a = next(
        x
        for x in Assignment.objects.filter(person=okafor.person, status="not_started")
        if len(FormSchema(x.form_version).visible_sections({})) > 2
    )
    s = FormSchema(a.form_version)
    rs.save_draft(a, okafor, {})
    done, total = section_progress(a, s)
    assert done == 0 and total >= 2

    optq = s.optout_question
    first = next(
        sec
        for sec in s.visible_sections({})
        if not sec.is_repeatable
        and not (optq and sec.pk == optq.form_section_id)
        and any(q.question_type != QuestionType.INSTRUCTIONS for q in sec.questions.all())
    )
    post = {
        f"q-{q.code}": _value(q)
        for q in first.questions.all()
        if q.question_type not in (QuestionType.INSTRUCTIONS, QuestionType.FILE)
    }
    rs.save_draft(a, okafor, post)
    a.refresh_from_db()
    assert section_progress(a, FormSchema(a.form_version)) == (1, total)


def test_started_form_shows_sections_done(client, okafor):
    a = next(
        x
        for x in Assignment.objects.filter(person=okafor.person, status="not_started")
        if len(FormSchema(x.form_version).visible_sections({})) > 2
    )
    rs.save_draft(a, okafor, {})
    client.force_login(okafor)
    html = client.get("/tasks/").content.decode()
    row = _row(html, a)
    assert "sections. Your answers" not in row  # nothing filled in yet: no count (MW 2026-10-27)
    assert "You previously started this" in row

    s = FormSchema(a.form_version)
    sec = next(
        x
        for x in s.visible_sections({})
        if not x.is_repeatable
        and not (s.optout_question and x.pk == s.optout_question.form_section_id)
        and any(q.question_type != QuestionType.INSTRUCTIONS for q in x.questions.all())
    )
    rs.save_draft(
        a,
        okafor,
        {
            f"q-{q.code}": _value(q)
            for q in sec.questions.all()
            if q.question_type not in (QuestionType.INSTRUCTIONS, QuestionType.FILE)
        },
    )
    html = client.get("/tasks/").content.decode()
    assert "sections.<br>Your answers are saved." in _row(html, a)


def _next_card(html):
    i = html.index('class="welcome-next"')
    return html[i : html.index("</a>", i)]


def test_next_up_finishes_a_started_survey_first_then_the_publications_review(client, okafor):
    """Next up (MW 2026-11-24): a started survey first; otherwise the publications review; otherwise the first task."""
    from django.urls import reverse

    from apps.portal.outcome_views import task_item

    person = okafor.person
    mine = Assignment.objects.filter(person=person, reporting_period__status="open")
    mine.update(status="not_started")
    client.force_login(okafor)

    html = client.get("/tasks/").content.decode()
    card = _next_card(html)
    oc = task_item(person, ReportingPeriod.objects.get(status="open"))
    if oc and not oc["done"]:
        assert reverse("portal:outcomes") in card
        assert "publications, talks, and grants" in card
    else:
        assert "/tasks/" in card and "Start" in card

    a = next(x for x in mine if f"/tasks/{x.pk}/" in html)
    rs.save_draft(a, okafor, {})
    a.refresh_from_db()
    assert a.status == "in_progress"
    card = _next_card(client.get("/tasks/").content.decode())
    assert f"/tasks/{a.pk}/" in card
    assert "Continue" in card
