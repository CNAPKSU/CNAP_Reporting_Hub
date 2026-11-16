"""Anonymous counts of Home link selections (MW 2026-11-15, approved), so the CNAP team can see after launch what
members use and trim the rest. Only the day, a short link label, and a running count are kept."""

import re
from collections import defaultdict
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.accounts import access
from apps.analytics.models import HomeLinkCount

_OK = re.compile(r"[^\w .,:’'&()/-]")


def clean_key(raw):
    """Keep a short, plain label. Anything else is dropped, so the table never holds free text from a page."""
    key = _OK.sub("", (raw or "").strip())[:160].strip()
    return key if len(key) >= 3 else ""


@csrf_exempt  # sent by navigator.sendBeacon, which can't add the CSRF header; it only adds one to a count
@require_POST
@login_required
def count(request):
    key = clean_key(request.POST.get("k"))
    if key:
        day = timezone.localdate()
        row, made = HomeLinkCount.objects.get_or_create(day=day, key=key, defaults={"count": 1})
        if not made:
            HomeLinkCount.objects.filter(pk=row.pk).update(count=F("count") + 1)
    return HttpResponse(status=204)


@login_required
def report(request):
    if not access.can_view_admin(request.user):
        raise PermissionDenied
    days = int(request.GET.get("days", 30)) if str(request.GET.get("days", "30")).isdigit() else 30
    since = timezone.localdate() - timedelta(days=days - 1)
    totals = defaultdict(int)
    for r in HomeLinkCount.objects.filter(day__gte=since):
        totals[r.key] += r.count
    rows = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
    return render(
        request,
        "manage/home_link_counts.html",
        {"rows": rows, "days": days, "since": since, "total": sum(totals.values())},
    )
