"""Requests to join the Member Hub (MW 2026-11-24, approved feature): the waiting list, Approve, and Decline."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

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
    return render(
        request,
        "manage/access_requests.html",
        {"pending": pending, "decided": decided, "notify": ar.notify_address()},
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
