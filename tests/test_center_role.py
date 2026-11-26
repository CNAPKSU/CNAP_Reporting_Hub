"""Add to the roster (MW 2026-11-25): "Title", the person's role in the Center, and a spreadsheet upload."""

import pytest
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apps.people import roster_import
from apps.people.models import Person

from .conftest import make_person, make_user, relate


@pytest.fixture
def evaluator(reference):
    u = make_user(
        make_person("Morgan", "Wills"), username="mw", role=reference["roles"]["administrator"]
    )
    u.user_permissions.add(Permission.objects.get(codename="view_identified_survey_responses"))
    return u


@pytest.fixture
def member(reference):
    p = make_person("Avery", "Sample")
    relate(p, reference["types"]["cnap_member"])
    return make_user(p, username="avery")


def test_add_person_page_says_title_and_offers_role_and_spreadsheet(client, evaluator):
    client.force_login(evaluator)
    page = client.get(reverse("manage:person_new")).content.decode()
    assert "Position title" not in page
    assert ">Title<" in page
    assert "Role in the Center" in page and "Core senior advisor" in page
    assert reverse("manage:roster_upload") in page
    assert reverse("manage:roster_template") in page


def test_add_person_with_several_roles_and_with_other(client, evaluator):
    client.force_login(evaluator)
    base = {"first_name": "Lee", "last_name": "Mentor", "institution": "Kansas State University"}
    client.post(
        reverse("manage:person_new"),
        {**base, "center_roles": ["core_director", "mentor"], "center_role_other": "ignored"},
    )
    p = Person.objects.get(last_name="Mentor")
    assert p.center_roles == ["mentor", "core_director"] and p.center_role_other == ""
    assert p.center_role_label == "Mentor, Core director"

    r = client.post(
        reverse("manage:person_new"), {**base, "last_name": "Blank", "center_roles": ["other"]}
    )
    assert r.status_code == 200 and "untick Other" in r.content.decode()
    assert not Person.objects.filter(last_name="Blank").exists()

    client.post(
        reverse("manage:person_new"),
        {
            **base,
            "last_name": "Visitor",
            "center_roles": ["mentor", "other"],
            "center_role_other": "Visiting scholar",
        },
    )
    assert Person.objects.get(last_name="Visitor").center_role_labels == [
        "Mentor",
        "Visiting scholar",
    ]


def test_member_sets_several_roles_on_profile(client, member):
    client.force_login(member)
    page = client.get(reverse("portal:profile")).content.decode()
    assert "Role in the Center" in page and "Position title" not in page
    assert 'type="checkbox" name="center_roles" value="center_director"' in page
    client.post(
        reverse("portal:profile"),
        {
            "department": "",
            "position_title": "",
            "center_roles_shown": "1",
            "center_roles": ["graduate_student", "core_staff"],
        },
    )
    member.person.refresh_from_db()
    assert member.person.center_roles == ["graduate_student", "core_staff"]
    page = client.get(reverse("portal:profile")).content.decode()
    assert 'value="graduate_student" checked' in page and 'value="core_staff" checked' in page

    client.post(
        reverse("portal:profile"),
        {"department": "", "position_title": "", "center_roles_shown": "1"},
    )
    member.person.refresh_from_db()
    assert member.person.center_roles == []


def test_profile_without_the_role_field_leaves_it_alone(client, member):
    Person.objects.filter(pk=member.person.pk).update(center_roles=["core_staff"])
    client.force_login(member)
    client.post(reverse("portal:profile"), {"department": "", "position_title": ""})
    member.person.refresh_from_db()
    assert member.person.center_roles == ["core_staff"]


def test_blank_spreadsheet_has_the_columns(client, evaluator):
    client.force_login(evaluator)
    r = client.get(reverse("manage:roster_template"))
    assert r.status_code == 200 and "attachment" in r["Content-Disposition"]
    head = r.content.decode("utf-8-sig").strip()
    assert head == ",".join(roster_import.TEMPLATE_HEADER)


def test_spreadsheet_reads_title_and_roles(evaluator):
    csv = (
        "First name,Last name,Email,Title,Role in the Center\n"
        'Ana,Lead,ana@example.edu,Associate Professor,"Research project leader; Mentor"\n'
        "Ben,Guest,ben@example.edu,,Other: Visiting scholar\n"
        "Cy,Plain,cy@example.edu,,\n"
    )
    imp = roster_import.parse(evaluator, SimpleUploadedFile("r.csv", csv.encode()))
    roster_import.commit(evaluator, imp)
    ana = Person.objects.get(last_name="Lead")
    assert ana.position_title == "Associate Professor"
    assert ana.center_roles == ["research_project_leader", "mentor"]
    ben = Person.objects.get(last_name="Guest")
    assert ben.center_roles == ["other"] and ben.center_role_other == "Visiting scholar"
    assert Person.objects.get(last_name="Plain").center_roles == []


def test_role_cells_are_matched_loosely():
    assert roster_import.center_role_fields("center director, MENTOR") == {
        "center_roles": ["mentor", "center_director"]
    }
    assert roster_import.center_role_fields("Postdoc") == {
        "center_roles": ["other"],
        "center_role_other": "Postdoc",
    }
    assert roster_import.center_role_fields("") == {}
