"""Anonymous Home link counts (MW 2026-11-15, approved). Fictional people only."""

import pytest
from django.core.management import call_command

from apps.accounts.models import User
from apps.analytics.models import HomeLinkCount
from apps.portal.clicks import clean_key


@pytest.fixture
def center(db):
    call_command("seed", "--fictional", verbosity=0)


def test_counts_are_anonymous_and_add_up(center, client):
    client.force_login(User.objects.get(username="okafor"))
    for _ in range(3):
        assert client.post("/hub/count/", {"k": "Funding: Grant resources"}).status_code == 204
    row = HomeLinkCount.objects.get(key="Funding: Grant resources")
    assert row.count == 3
    assert {f.name for f in HomeLinkCount._meta.fields} == {"id", "day", "key", "count"}  # nothing about the person


def test_signed_out_and_junk_are_not_counted(center, client):
    client.post("/hub/count/", {"k": "Funding: Grant resources"})
    assert not HomeLinkCount.objects.exists()
    assert clean_key("<script>x</script>") == "scriptx/script"  # angle brackets are dropped
    assert clean_key("ab") == ""


def test_only_administrators_see_the_counts(center, client):
    client.force_login(User.objects.get(username="okafor"))
    assert client.get("/hub/link-counts/").status_code == 403
    client.force_login(User.objects.get(username="mwills"))
    assert client.get("/hub/link-counts/").status_code == 200
