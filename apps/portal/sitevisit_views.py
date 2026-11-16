"""The Site Visit RSVP (MW 2026-11-15, approved build). One form a year per person, which the person can change
until the RSVP closes. A confirmation email repeats the answers. Staff see the counts and every RSVP."""

import csv
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from apps.audit.models import AuditLog, record_event
from apps.outcomes.models import SiteVisitRSVP

# The 2027 Site Visit (MW 2026-11-15). Kept here, beside the form, until the Site Visit has its own records.
YEAR = 2027
DATES = "Tuesday and Wednesday, May 25 and 26, 2027"
CLOSES = date(2027, 3, 25)
POSTER_BY = "Friday, April 23, 2027"
PARTS = [
    ("tue-am", "Tuesday, 8:40 a.m. to 1:15 p.m.", "Breakfast, the Center overview, core updates and discussion, group photographs, and lunch"),
    ("tue-tours", "Tuesday, 1:30 to 2:30 p.m.", "Guided tours of the cores and the CONNECT Lab"),
    ("tue-eac", "Tuesday, 2:45 to 4:00 p.m.", "Advisory committee meeting, closed session"),
    ("tue-eve", "Tuesday, 6:00 to 9:00 p.m.", "Keynote address and banquet"),
    ("wed-am", "Wednesday, 8:40 to 11:20 a.m.", "Breakfast, then the research project and pilot project presentations"),
    ("wed-posters", "Wednesday, 11:30 a.m. to 12:30 p.m.", "Poster session"),
]
MEALS = [("lunch", "Tuesday lunch, about halfway through the morning program"), ("dinner", "Tuesday dinner, the keynote address and banquet")]
NIGHTS = [("mon", "Monday night, May 24"), ("tue", "Tuesday night, May 25")]
CONNECTIONS = [
    "University or departmental leadership", "New or interested", "General member", "Mentor", "Pilot project leader",
    "Primary research project leader", "Core director", "External Advisory Committee member", "Graduate student",
    "Postdoctoral fellow", "Other",
]


def _yesno(v):
    return {"yes": True, "no": False}.get(v)


def _words(text):
    return len(text.split())


@login_required
def rsvp(request):
    me = getattr(request.user, "person", None)
    if not me:
        raise PermissionDenied("The Site Visit RSVP belongs to CNAP members.")
    existing = SiteVisitRSVP.objects.filter(person=me, year=YEAR).first()
    closed = date.today() > CLOSES
    errors = []
    if request.method == "POST" and not closed:
        p = request.POST
        attend = p.get("attend", "")
        if attend not in SiteVisitRSVP.Attend.values:
            errors.append("Please choose how you will attend.")
        abstract = p.get("poster_abstract", "").strip()
        if _words(abstract) > 150:
            errors.append(f"Please shorten the abstract to 150 words. It has {_words(abstract)} now.")
        if not errors:
            here = attend == "person"
            data = dict(
                attend=attend,
                parts=[k for k, _, _ in PARTS if here and k in p.getlist("parts")],
                meals=[k for k, _ in MEALS if here and k in p.getlist("meals")],
                diet=p.get("diet", "").strip() if here else "",
                photo_ok=_yesno(p.get("photo_ok")) if here else None,
                parking={"drive": True, "nodrive": False}.get(p.get("parking")) if here else None,
                hotel_nights=[k for k, _ in NIGHTS if here and k in p.getlist("hotel_nights")],
                poster=p.get("poster", "") if attend != "no" and p.get("poster") in SiteVisitRSVP.Poster.values else "",
                poster_title=p.get("poster_title", "").strip(),
                poster_authors=p.get("poster_authors", "").strip()[:500],
                poster_affiliation=p.get("poster_affiliation", "").strip()[:300],
                poster_abstract=abstract,
                name_tag=p.get("name_tag", "").strip()[:80] if attend != "no" else "",
                connection=p.get("connection", "") if p.get("connection") in CONNECTIONS else "",
                note=p.get("note", "").strip(),
            )
            if data["poster"] not in ("yes", "done"):
                data.update(poster_title="", poster_authors="", poster_affiliation="", poster_abstract="")
            if existing:
                old = {k: getattr(existing, k) for k in data}
                for k, v in data.items():
                    setattr(existing, k, v)
                existing.save()
                r = existing
                record_event(request.user, AuditLog.Action.UPDATE, r, old=old, new=data)
            else:
                r = SiteVisitRSVP.objects.create(person=me, year=YEAR, **data)
                record_event(request.user, AuditLog.Action.CREATE, r, new=data)
            _confirm(r)
            messages.success(request, "Thank you. Your RSVP is saved, and a confirmation email is on the way.")
            return redirect(reverse("portal:sitevisit_rsvp") + "#done")
    from . import hub

    return render(
        request,
        "hub/sitevisit_rsvp.html",
        {
            **hub.chrome(request),
            "r": existing,
            "attend_now": (request.POST.get("attend") if errors else None) or (existing.attend if existing else "person"),
            "post": request.POST if errors else None,
            "errors": errors,
            "closed": closed,
            "year": YEAR,
            "dates": DATES,
            "closes": CLOSES,
            "poster_by": POSTER_BY,
            "parts": PARTS,
            "meals": MEALS,
            "nights": NIGHTS,
            "connections": CONNECTIONS,
        },
    )


def _summary(r):
    label = dict((k, f"{d}: {t}") for k, d, t in PARTS)
    lines = [f"How you will attend: {r.get_attend_display()}"]
    if r.attend == "person":
        lines.append("Parts of the program: " + ("; ".join(label[k] for k in r.parts) or "None chosen"))
        lines.append("Meals: " + (", ".join(dict(MEALS)[k] for k in r.meals) or "Neither"))
        lines.append("Dietary needs: " + (r.diet or "None"))
        lines.append("Photographs: " + {True: "Yes, you may use my image", False: "No, please don’t use my image", None: "Not answered"}[r.photo_ok])
        lines.append("Parking: " + {True: "Needs parking", False: "No parking needed", None: "Not answered"}[r.parking])
        lines.append("Hotel nights: " + (", ".join(dict(NIGHTS)[k] for k in r.hotel_nights) or "None"))
    if r.poster:
        lines.append("Poster session: " + r.get_poster_display())
    if r.poster_title:
        lines.append("Poster title: " + r.poster_title)
    if r.name_tag:
        lines.append("Name tag: " + r.name_tag)
    if r.note:
        lines.append("Anything else: " + r.note)
    return lines


# The two Site Visit days for the calendar file (MW 2026-11-15: the confirmation email carries a calendar file)
ICS_DAYS = [("20270525T084000", "20270525T210000", "2027 CNAP Site Visit, day 1"), ("20270526T084000", "20270526T123000", "2027 CNAP Site Visit, day 2")]


def calendar_file(r):
    """A small .ics file with both Site Visit days, in Central time, for Outlook, Google Calendar, or Apple Calendar."""
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//CNAP Member Hub//Site Visit RSVP//EN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH"]
    for i, (start, end, title) in enumerate(ICS_DAYS, start=1):
        lines += [
            "BEGIN:VEVENT",
            f"UID:cnap-site-visit-{r.year}-day{i}-person{r.person_id}@cnap.k-state.edu",
            "DTSTAMP:" + r.updated_at.strftime("%Y%m%dT%H%M%SZ"),
            f"DTSTART;TZID=America/Chicago:{start}",
            f"DTEND;TZID=America/Chicago:{end}",
            f"SUMMARY:{title}",
            "LOCATION:Kansas State University\\, Manhattan\\, Kansas",
            "DESCRIPTION:The program and your RSVP are in the CNAP Member Hub.",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def _confirm(r):
    email = r.person.primary_email
    if not email:
        return
    msg = EmailMessage(
        subject=f"Your RSVP for the {r.year} CNAP Site Visit",
        body=render_to_string(
            "email/sitevisit_rsvp.txt",
            {"r": r, "lines": _summary(r), "dates": DATES, "poster_by": POSTER_BY, "url": settings.SITE_URL + reverse("portal:sitevisit_rsvp"), "ics": r.attend != "no"},
        ),
        to=[email],
    )
    if r.attend != "no":
        msg.attach(f"cnap-site-visit-{r.year}.ics", calendar_file(r), "text/calendar")
    msg.send()


def staff_list(request):
    """Counts and every RSVP, for the CNAP team (any administrator may look). CSV with ?format=csv."""
    from apps.accounts import access

    if not request.user.is_authenticated or not access.can_view_admin(request.user):
        raise PermissionDenied
    rs = list(SiteVisitRSVP.objects.filter(year=YEAR).select_related("person"))
    if request.GET.get("format") == "csv":
        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = f'attachment; filename="site-visit-{YEAR}-rsvps.csv"'
        w = csv.writer(resp)
        w.writerow(["Name", "Email", "Attending", "Lunch", "Dinner", "Dietary needs", "Photographs OK", "Parking", "Monday night", "Tuesday night", "Poster", "Poster title", "Name tag", "Connection", "Anything else", "Updated"])
        for r in rs:
            w.writerow([r.person.full_name, r.person.primary_email, r.get_attend_display(), "lunch" in r.meals, "dinner" in r.meals, r.diet,
                        {True: "Yes", False: "No", None: ""}[r.photo_ok], {True: "Yes", False: "No", None: ""}[r.parking],
                        "mon" in r.hotel_nights, "tue" in r.hotel_nights, r.get_poster_display() if r.poster else "", r.poster_title, r.name_tag, r.connection, r.note, r.updated_at.date()])
        return resp
    counts = {
        "person": sum(r.attend == "person" for r in rs),
        "zoom": sum(r.attend == "zoom" for r in rs),
        "no": sum(r.attend == "no" for r in rs),
        "lunch": sum("lunch" in r.meals for r in rs),
        "dinner": sum("dinner" in r.meals for r in rs),
        "mon": sum("mon" in r.hotel_nights for r in rs),
        "tue": sum("tue" in r.hotel_nights for r in rs),
        "parking": sum(r.parking is True for r in rs),
        "posters": sum(r.poster in ("yes", "done") for r in rs),
        "diet": sum(bool(r.diet) for r in rs),
    }
    return render(request, "manage/sitevisit_rsvps.html", {"rs": rs, "counts": counts, "year": YEAR})
