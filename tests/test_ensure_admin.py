"""The first administrator for the Render launch (MW 2026-11-24)."""

import pytest
from django.core.management import call_command

from apps.accounts import access
from apps.accounts.models import User


@pytest.mark.django_db
def test_ensure_admin_creates_once_and_is_safe_to_repeat(monkeypatch):
    call_command("seed", verbosity=0)
    monkeypatch.setenv("ADMIN_EMAIL", "first.admin@example.edu")
    monkeypatch.setenv("ADMIN_FIRST_NAME", "First")
    monkeypatch.setenv("ADMIN_LAST_NAME", "Admin")
    call_command("ensure_admin")
    call_command("ensure_admin")
    users = User.objects.filter(email="first.admin@example.edu")
    assert users.count() == 1
    u = users.get()
    assert access.can_view_admin(u)
    assert not u.has_usable_password()


@pytest.mark.django_db
def test_ensure_admin_skips_without_settings(monkeypatch):
    for k in ("ADMIN_EMAIL", "ADMIN_FIRST_NAME", "ADMIN_LAST_NAME"):
        monkeypatch.delenv(k, raising=False)
    before = User.objects.count()
    call_command("ensure_admin")
    assert User.objects.count() == before


def test_health_check_answers_without_sign_in(client):
    r = client.get("/healthz")
    assert r.status_code == 200 and r.content == b"ok"
