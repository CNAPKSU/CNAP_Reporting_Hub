"""Requests to join the Member Hub (MW 2026-11-24, approved feature).

Anyone may ask; nothing is created until an administrator approves. The public page always gives the same reply,
so it never reveals who is already a member. Someone already on file who asks is simply sent a sign-in link.
"""

from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

from apps.audit.models import AuditLog, record_event
from apps.people.models import Person, PersonEmail

from . import signin
from .models import AccessRequest

REQUESTS_PER_IP_HOUR = 5


def notify_address():
    return getattr(settings, "ACCESS_REQUEST_NOTIFY", "") or settings.EVALUATOR_EMAIL


def submit(data, ip=None):
    """Record a request, or quietly do nothing (throttled, a bot, a duplicate, or already a member)."""
    if data.get("website"):  # left empty by people; bots fill every box
        return None
    first = (data.get("first_name") or "").strip()[:100]
    last = (data.get("last_name") or "").strip()[:100]
    email = (data.get("email") or "").strip().lower()[:254]
    if not (first and last and "@" in email):
        return None
    if (
        ip
        and AccessRequest.objects.filter(
            ip=ip, created_at__gte=timezone.now() - timedelta(hours=1)
        ).count()
        >= REQUESTS_PER_IP_HOUR
    ):
        return None
    if PersonEmail.objects.filter(email__iexact=email).exists():
        signin.request_link(email, ip=ip)  # already a member: send a sign-in link instead
        return None
    if AccessRequest.objects.filter(
        email__iexact=email, status=AccessRequest.Status.PENDING
    ).exists():
        return None
    req = AccessRequest.objects.create(
        first_name=first,
        last_name=last,
        email=email,
        department=(data.get("department") or "").strip()[:200],
        connection=(data.get("connection") or "").strip()[:300],
        note=(data.get("note") or "").strip()[:2000],
        ip=ip,
    )
    record_event(None, AuditLog.Action.CREATE, req, new={"access_request": email})
    send_mail(
        subject=f"Member Hub access request: {first} {last}",
        message=render_to_string(
            "email/access_request_staff.txt", {"r": req, "site": settings.SITE_URL}
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[notify_address()],
        fail_silently=True,
    )
    return req


@transaction.atomic
def approve(req, actor):
    """Make the person (or use the one already on file) and e-mail a welcome sign-in link."""
    if req.status != AccessRequest.Status.PENDING:
        return None
    row = PersonEmail.objects.filter(email__iexact=req.email).select_related("person").first()
    if row:
        person = row.person
    else:
        person = Person.objects.create(
            first_name=req.first_name, last_name=req.last_name, department=req.department
        )
        PersonEmail.objects.create(person=person, email=req.email, is_primary=True)
        record_event(actor, AuditLog.Action.CREATE, person, new={"from_access_request": req.pk})
    req.status = AccessRequest.Status.APPROVED
    req.decided_at = timezone.now()
    req.decided_by = actor
    req.person = person
    req.save(update_fields=["status", "decided_at", "decided_by", "person", "updated_at"])
    record_event(actor, AuditLog.Action.UPDATE, req, new={"status": "approved"})
    if signin.may_use_link(person):
        url = signin.make_link(person, req.email, "welcome")
        send_mail(
            subject="Welcome to the CNAP Member Hub",
            message=render_to_string(
                "email/access_request_welcome.txt",
                {"person": person, "url": url, "days": signin.LINK_DAYS, "site": settings.SITE_URL},
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[req.email],
            fail_silently=True,
        )
    return person


def decline(req, actor):
    """Mark the request declined. No e-mail goes out; the CNAP team replies personally if needed."""
    if req.status != AccessRequest.Status.PENDING:
        return
    req.status = AccessRequest.Status.DECLINED
    req.decided_at = timezone.now()
    req.decided_by = actor
    req.save(update_fields=["status", "decided_at", "decided_by", "updated_at"])
    record_event(actor, AuditLog.Action.UPDATE, req, new={"status": "declined"})
