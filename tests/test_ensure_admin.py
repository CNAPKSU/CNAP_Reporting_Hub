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
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)
    call_command("ensure_admin")
    call_command("ensure_admin")
    users = User.objects.filter(email="first.admin@example.edu")
    assert users.count() == 1
    u = users.get()
    assert access.can_view_admin(u)
    assert not u.has_usable_password()


@pytest.mark.django_db
def test_ensure_admin_skips_without_settings(monkeypatch):
    for k in ("ADMIN_EMAIL", "ADMIN_FIRST_NAME", "ADMIN_LAST_NAME", "ADMIN_PASSWORD"):
        monkeypatch.delenv(k, raising=False)
    before = User.objects.count()
    call_command("ensure_admin")
    assert User.objects.count() == before


def test_health_check_answers_without_sign_in(client):
    r = client.get("/healthz")
    assert r.status_code == 200 and r.content == b"ok"


@pytest.mark.django_db
def test_ensure_admin_sets_the_first_password_once_and_never_overwrites(monkeypatch):
    call_command("seed", verbosity=0)
    monkeypatch.setenv("ADMIN_EMAIL", "first.admin@example.edu")
    monkeypatch.setenv("ADMIN_FIRST_NAME", "First")
    monkeypatch.setenv("ADMIN_LAST_NAME", "Admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "Long-First-Password-2026")
    call_command("ensure_admin")
    u = User.objects.get(email="first.admin@example.edu")
    assert u.check_password("Long-First-Password-2026")
    u.set_password("Changed-By-The-Admin-2026")
    u.save()
    call_command("ensure_admin")
    u.refresh_from_db()
    assert u.check_password("Changed-By-The-Admin-2026")
