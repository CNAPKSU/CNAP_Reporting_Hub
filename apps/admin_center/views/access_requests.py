"""Requests to join the Member Hub (MW 2026-11-24, approved feature): the waiting list, Approve, and Decline."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.accounts import access_requests as ar
from apps.accounts.models import AccessRequest

from ..decorators import admin_view, manage_action


@admin_view
def access_requests(request):
    pending = AccessRequest.objects.filter(status=AccessRequest.Status.PENDING).order_by(
        "created_at"
    )
    decided = AccessRequest.objects.exclude(status=AccessRequest.Status.PENDING).select_related(
        "decided_by", "person"
    )[:50]
    from apps.reporting.services import roster_check as rc

    return render(
        request,
        "manage/access_requests.html",
        {
            "pending": pending,
            "decided": decided,
            "notify": ar.notify_address(),
            "role_requests": rc.own_pending(),
        },
    )


@manage_action
def access_request_decide(request, pk):
    req = get_object_or_404(AccessRequest, pk=pk)
    if request.POST.get("decision") == "approve":
        person = ar.approve(req, request.user)
        if person:
            messages.success(
                request,
                f"Approved. {person} is in the Hub and has a welcome sign-in link.\n"
                "Add their CNAP role and relationships on their page.",
            )
            return redirect("manage:person", person.pk)
    elif request.POST.get("decision") == "decline":
        ar.decline(req, request.user)
        messages.success(request, f"Declined the request from {req.first_name} {req.last_name}.")
    return redirect("manage:access_requests")


@manage_action
def role_request_decide(request, pk):
    """Handle a member's own request to change their roles (MW 2026-11-24, approved feature)."""
    from apps.reporting.models import RosterSuggestion
    from apps.reporting.services import roster_check as rc

    sg = get_object_or_404(RosterSuggestion, pk=pk, link__isnull=True)
    status = request.POST.get("decision", "")
    if status in ("done", "declined", "pending"):
        rc.decide(request.user, sg, status)
        messages.success(
            request,
            {"done": "Marked as handled.", "declined": "Declined.", "pending": "Back on the list."}[
                status
            ],
        )
    return redirect(reverse("manage:access_requests") + "#roles")
