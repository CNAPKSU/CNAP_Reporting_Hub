"""The Center calendar (MW 2026-11-27): add, edit, publish, and cancel events; review emailed drafts."""

from django import forms
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from apps.audit.models import AuditLog, record_event
from apps.events import feed
from apps.events.models import CenterEvent

from ..decorators import admin_view, manage_action


class EventForm(forms.ModelForm):
    class Meta:
        model = CenterEvent
        fields = ["title", "day", "end_day", "starts", "ends", "place", "url", "details"]
        labels = {
            "title": "Title",
            "day": "Date",
            "end_day": "Last day, if it runs several days",
            "starts": "Starts",
            "ends": "Ends",
            "place": "Where",
            "url": "More information (a link)",
            "details": "Details",
        }
        widgets = {
            "day": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_day": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "starts": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "ends": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "details": forms.Textarea(attrs={"rows": 3}),
            "url": forms.URLInput(attrs={"placeholder": "Blank: people go to the Events page"}),
        }
        help_texts = {
            "starts": "Leave blank for an all-day event.",
            "end_day": "",
            "url": "",
            "day": "",
        }

    def clean(self):
        d = super().clean()
        day, last = d.get("day"), d.get("end_day")
        if day and last:
            if last < day:
                self.add_error("end_day", "The last day can't come before the first day.")
            elif last == day:
                d["end_day"] = None
        if d.get("ends") and not d.get("starts"):
            self.add_error(
                "starts", "Add a start time, or clear the end time for an all-day event."
            )
        if d.get("starts") and d.get("ends") and not d.get("end_day") and d["ends"] <= d["starts"]:
            self.add_error("ends", "The end time should come after the start time.")
        return d


def _when(e):
    from apps.portal.hub import _clock

    day = f"{e.day:%A, %B} {e.day.day}"
    if e.end_day:
        day += f" to {e.end_day:%A, %B} {e.end_day.day}"
    if e.starts:
        day += f", {_clock(e.starts)}" + (f" to {_clock(e.ends)}" if e.ends else "")
    return day


@admin_view
def calendar(request):
    today = timezone.localdate()
    qs = CenterEvent.objects.all()
    editing = None
    if request.GET.get("edit"):
        editing = get_object_or_404(CenterEvent, pk=request.GET["edit"])
    form = EventForm(instance=editing) if editing else EventForm()
    rows = lambda q: [{"e": e, "when": _when(e)} for e in q]  # noqa: E731
    return render(
        request,
        "manage/calendar.html",
        {
            "form": form,
            "editing": editing,
            "drafts": rows(qs.filter(status=CenterEvent.Status.DRAFT).order_by("-created_at")),
            "upcoming": rows(
                qs.filter(status=CenterEvent.Status.PUBLISHED)
                .exclude(end_day__lt=today)
                .exclude(end_day__isnull=True, day__lt=today)
            ),
            "past": rows(
                qs.exclude(status=CenterEvent.Status.DRAFT)
                .filter(day__lt=today)
                .order_by("-day")[:60]
            ),
            "cancelled_upcoming": rows(
                qs.filter(status=CenterEvent.Status.CANCELLED, day__gte=today)
            ),
            "sync": feed.subscribe_links(),
            "inbound_address": getattr(settings, "CALENDAR_INBOUND_ADDRESS", ""),
            "inbound_webhook": feed.site() + feed.inbound_path(),
        },
    )


@manage_action
def calendar_save(request):
    pk = request.POST.get("pk")
    e = get_object_or_404(CenterEvent, pk=pk) if pk else None
    form = EventForm(request.POST, instance=e)
    if not form.is_valid():
        for k, v in form.errors.items():
            label = form.fields[k].label if k in form.fields else ""
            messages.error(request, f"{label}: {v[0]}" if label else v[0])
        return redirect(reverse("manage:calendar") + (f"?edit={pk}" if pk else ""))
    obj = form.save(commit=False)
    publish = request.POST.get("go") == "publish"
    if not pk:
        obj.created_by = request.user
        obj.status = CenterEvent.Status.PUBLISHED if publish else CenterEvent.Status.DRAFT
    elif publish:
        obj.status = CenterEvent.Status.PUBLISHED
    obj.check_date = False
    obj.save()
    record_event(
        request.user,
        AuditLog.Action.CREATE if not pk else AuditLog.Action.UPDATE,
        obj,
        new={"event": obj.title, "status": obj.status},
    )
    if obj.status == CenterEvent.Status.PUBLISHED:
        messages.success(
            request,
            f"“{obj.title}” is on the calendar. Subscribed calendars pick it up at their next check.",
        )
    else:
        messages.success(request, f"Saved “{obj.title}” as a draft. It isn’t on the calendar yet.")
    return redirect("manage:calendar")


@manage_action
def calendar_status(request, pk):
    e = get_object_or_404(CenterEvent, pk=pk)
    act = request.POST.get("act")
    old = e.status
    if act == "publish":
        e.status = CenterEvent.Status.PUBLISHED
        e.check_date = False
        msg = f"“{e.title}” is on the calendar."
    elif act == "cancel":
        e.status = CenterEvent.Status.CANCELLED
        msg = f"Cancelled “{e.title}”. It leaves subscribed calendars at their next check."
    elif act == "restore":
        e.status = CenterEvent.Status.PUBLISHED
        msg = f"“{e.title}” is back on the calendar."
    elif act == "discard" and e.status == CenterEvent.Status.DRAFT:
        record_event(
            request.user, AuditLog.Action.ARCHIVE, e, old={"event": e.title, "discarded": True}
        )
        e.delete()
        messages.success(request, "Discarded the draft.")
        return redirect("manage:calendar")
    else:
        return redirect("manage:calendar")
    e.save()
    record_event(
        request.user, AuditLog.Action.UPDATE, e, old={"status": old}, new={"status": e.status}
    )
    messages.success(request, msg)
    return redirect("manage:calendar")
