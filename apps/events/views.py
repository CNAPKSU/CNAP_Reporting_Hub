import json
import logging
import re

from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.accounts import access
from apps.accounts.signin import person_for_email
from apps.audit.models import AuditLog, record_event

from . import feed, inbound
from .models import CenterEvent

logger = logging.getLogger(__name__)


@never_cache
def calendar_feed(request, key):
    """The subscribable feed. No sign-in, because calendar apps can't sign in; the key in the
    address is the lock (MW 2026-11-27)."""
    if not feed.key_ok(key):
        raise Http404
    resp = HttpResponse(feed.ics(), content_type="text/calendar; charset=utf-8")
    resp["Content-Disposition"] = 'inline; filename="cnap-calendar.ics"'
    return resp


@csrf_exempt
@require_POST
def calendar_inbound(request, key):
    """Postmark's inbound webhook: an emailed event becomes a draft on the Calendar page.

    Always answers 200 for a good key, so Postmark doesn't retry an email we chose to ignore."""
    if not feed.inbound_key_ok(key):
        raise Http404
    try:
        msg = json.loads(request.body.decode("utf-8") or "{}")
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "why": "not JSON"})
    sender = ((msg.get("FromFull") or {}).get("Email") or msg.get("From") or "").strip()
    if "<" in sender:
        sender = sender.split("<", 1)[1].rstrip(">").strip()
    person = person_for_email(sender)
    user = getattr(person, "user", None) if person else None
    if not user or not user.is_enabled or not access.can_manage(user):
        logger.warning("Calendar email from %s ignored: not someone who manages the Hub.", sender)
        return JsonResponse({"ok": False, "why": "sender not allowed"})
    body = msg.get("StrippedTextReply") or msg.get("TextBody") or ""
    if not body.strip() and msg.get("HtmlBody"):
        body = re.sub(r"<[^>]+>", " ", msg["HtmlBody"])
        body = re.sub(r"[ \t]+", " ", body)
    d = inbound.parse(msg.get("Subject", ""), body)
    e = CenterEvent.objects.create(
        **d,
        status=CenterEvent.Status.DRAFT,
        source=CenterEvent.Source.EMAIL,
        email_from=sender[:254],
        email_subject=(msg.get("Subject") or "")[:300],
        email_body=body[:20000],
        created_by=user,
    )
    record_event(user, AuditLog.Action.CREATE, e, new={"event": e.title, "by_email": True})
    link = feed.site() + reverse("manage:calendar") + f"?edit={e.pk}"
    when = f"{e.day:%A, %B} {e.day.day}, {e.day.year}"
    try:
        send_mail(
            subject=f"Draft ready: {e.title}",
            message=(
                f"Your event is waiting as a draft on the Hub's Calendar page:\n\n{e.title}\n"
                + (
                    "No clear date was in the email, so please set one.\n"
                    if e.check_date
                    else f"{when}\n"
                )
                + f"\nCheck it and publish it here:\n{link}\n\n"
                "Nothing reaches members' calendars until you publish it.\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sender],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Couldn't confirm the calendar draft to %s", sender)
    return JsonResponse({"ok": True, "draft": e.pk})
