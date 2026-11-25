"""TEMPORARY (design review only; removed before the PR): render Hub pages with the fictional seed and save the HTML."""

import os
import sys
from pathlib import Path

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")
sys.path.insert(0, os.getcwd())
django.setup()

from django.core.management import call_command  # noqa: E402
from django.test import Client, override_settings  # noqa: E402
from django.urls import reverse  # noqa: E402

from apps.accounts.models import User  # noqa: E402
from apps.portal.hub_pages import PAGES, url_name  # noqa: E402

call_command("migrate", verbosity=0)
call_command("seed", "--fictional", verbosity=0)
try:
    call_command("seed_funding", verbosity=0)
except Exception as e:  # the funding seed is optional for previews
    print("seed_funding:", e)
from apps.outcomes import funding  # noqa: E402

funding.load_questions()

OUT = Path("rendered")
pages = [
    "/",
    "/funding/",
    "/funding/resources/",
    "/funding/news/",
    "/outcomes/",
    "/history/",
    "/tasks/",
]
pages += [reverse(f"portal:{url_name(k)}") for k in PAGES]
with override_settings(UI_PROTOTYPE=True, UI_PROTOTYPE_ONLY=True, DEBUG=False):
    for username in ("mwills", "okafor"):
        c = Client()
        c.force_login(User.objects.get(username=username))
        for p in pages:
            r = c.get(p)
            name = (p.strip("/").replace("/", "__") or "home") + ".html"
            d = OUT / username
            d.mkdir(parents=True, exist_ok=True)
            (d / name).write_bytes(r.content)
            print(username, r.status_code, p)
