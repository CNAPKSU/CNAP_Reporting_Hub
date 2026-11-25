"""Values every template needs: what the signed-in person may see and do."""

from django.conf import settings

from apps.accounts import access


def role_summary(rels):
    """Plain description of someone's CNAP roles for the sidebar, e.g. 'BN Core Director'."""
    parts = []
    for r in rels:
        if r.relationship_type.code == "cnap_member":
            continue
        name = r.relationship_type.name.replace(" (RPL)", "").replace(" (PPL)", "")
        if r.core_id:
            name = f"{r.core.code} {name}"
        if name not in parts:
            parts.append(name)
    return " · ".join(parts) or "CNAP member"


def cnap(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        from .models import SitePhoto

        return {
            "platform_name": "CNAP Member Hub",
            "evaluator_email": settings.EVALUATOR_EMAIL,
            "site_photo": SitePhoto.current(),
            "demo_site": getattr(settings, "DEMO_SITE", False),
            "proto_only": getattr(settings, "UI_PROTOTYPE_ONLY", False),
        }
    person = getattr(user, "person", None)
    rels = (
        list(person.current_relationships().select_related("relationship_type", "core"))
        if person
        else []
    )
    has_roles = bool(rels)
    label = access.admin_label(user)
    if not access.can_view_admin(user):
        label = role_summary(rels)
    from apps.outcomes.services import owners_for

    keeps_outcomes = bool(person and owners_for(person))
    return {
        "platform_name": "CNAP Member Hub",
        "evaluator_email": settings.EVALUATOR_EMAIL,
        "keeps_outcomes": keeps_outcomes,
        "can_view_admin": access.can_view_admin(user),
        "can_manage": access.can_manage(user),
        # Requests to join, waiting for an administrator (MW 2026-11-24)
        "access_requests_waiting": _waiting_requests(user),
        "is_view_only_admin": access.is_view_only_admin(user),
        "access_label": label,
        "has_cnap_roles": has_roles,
        "demo_site": getattr(settings, "DEMO_SITE", False),
        "proto_only": getattr(settings, "UI_PROTOTYPE_ONLY", False),
        # Core directors get a "Core reports" link (MW 2026-11-08).
        "directs_core": any(
            r.relationship_type.code == "core_director" and r.core_id for r in rels
        ),
    }


def _waiting_requests(user):
    if not access.can_view_admin(user):
        return 0
    from apps.accounts.models import AccessRequest
    from apps.reporting.services.roster_check import own_pending

    return AccessRequest.objects.filter(status=AccessRequest.Status.PENDING).count() + (
        own_pending().count()
    )
