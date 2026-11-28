"""The Center calendar as one subscribable iCalendar feed (MW 2026-11-27).

Calendar apps can't sign in, so the feed's address carries a long secret key. Members subscribe once;
Outlook and Google then fetch the feed on their own schedule, so new, changed, and cancelled events
follow automatically. Each item keeps a fixed UID and a SEQUENCE that grows when it changes, so an edit
updates the event in people's calendars instead of adding a copy.
"""

import hashlib
import hmac
from datetime import date, datetime, time, timedelta
from urllib.parse import quote
from zoneinfo import ZoneInfo

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

CENTRAL = ZoneInfo("America/Chicago")
NAME = "CNAP Center calendar"
NEUROSYNC_PLACE = "Leadership Room 127"
WINDOW_BACK = timedelta(days=120)


def feed_key():
    key = getattr(settings, "CALENDAR_FEED_KEY", "") or ""
    if key:
        return key
    return hmac.new(
        settings.SECRET_KEY.encode(), b"cnap-calendar-feed", hashlib.sha256
    ).hexdigest()[:40]


def key_ok(key):
    return hmac.compare_digest(str(key), feed_key())


def site():
    return getattr(settings, "SITE_URL", "").rstrip("/")


def feed_url():
    return site() + reverse("calendar_feed", args=[feed_key()])


def subscribe_links():
    """Everything the Sync box needs: the address itself and one-click links for each calendar app."""
    https = feed_url()
    webcal = "webcal://" + https.split("://", 1)[-1]
    return {
        "url": https,
        "webcal": webcal,
        "outlook": "https://outlook.office.com/calendar/0/addfromweb?url="
        + quote(https, safe="")
        + "&name="
        + quote(NAME, safe=""),
        "google": "https://calendar.google.com/calendar/r?cid=" + quote(webcal, safe=""),
    }


# -- the items ---------------------------------------------------------------------------------------
def _seq(dt):
    return int(dt.timestamp()) if dt else 0


def items(today=None):
    """Every dated item on the Center calendar, oldest first, as plain dicts."""
    from apps.outcomes import funding
    from apps.reporting.models import ReportingPeriod, SpeakerTalk

    from .models import CenterEvent

    today = today or timezone.localdate()
    since = today - WINDOW_BACK
    base = site()
    out = []
    for e in CenterEvent.objects.filter(
        status=CenterEvent.Status.PUBLISHED, day__gte=since - timedelta(days=60)
    ):
        if e.last_day < since:
            continue
        out.append(
            {
                "uid": f"event-{e.uid}@cnap-hub",
                "seq": _seq(e.updated_at),
                "stamp": e.updated_at,
                "title": e.title,
                "day": e.day,
                "last_day": e.last_day,
                "starts": e.starts,
                "ends": e.ends,
                "place": e.place,
                "details": e.details,
                "url": e.url or base + reverse("portal:hub_events"),
                "kind": "ctr",
            }
        )
    ns_url = base + reverse("portal:hub_neurosync")
    for t in SpeakerTalk.objects.filter(ends_at__date__gte=since).select_related("speaker"):
        end = timezone.localtime(t.ends_at, CENTRAL)
        start = end - timedelta(hours=1)
        who = f"{t.speaker.first_name} {t.speaker.last_name}".strip()
        out.append(
            {
                "uid": f"talk-{t.pk}@cnap-hub",
                "seq": _seq(t.updated_at),
                "stamp": t.updated_at,
                "title": f"NeuroSync: {t.title}" + (f" ({who})" if who else ""),
                "day": start.date(),
                "last_day": start.date(),
                "starts": start.time(),
                "ends": end.time(),
                "place": NEUROSYNC_PLACE,
                "details": "NeuroSync Weekly Speaker Series. Refreshments are provided.",
                "url": ns_url,
                "kind": "ns",
            }
        )
    tasks = base + reverse("portal:tasks")
    for p in ReportingPeriod.objects.filter(
        status__in=["open", "closed", "finalized"], due_at__date__gte=since
    ):
        d = timezone.localtime(p.due_at, CENTRAL).date()
        out.append(
            {
                "uid": f"due-{p.pk}@cnap-hub",
                "seq": _seq(p.updated_at),
                "stamp": p.updated_at,
                "title": f"CNAP reporting due: {p.name}",
                "day": d,
                "last_day": d,
                "starts": None,
                "ends": None,
                "place": "",
                "details": "Your surveys and reports for this session are under My tasks in the CNAP Member Hub.",
                "url": tasks,
                "kind": "due",
            }
        )
    fund = base + reverse("portal:funding")
    for e in funding.upcoming_events(since):
        out.append(
            {
                "uid": f"funding-event-{e.pk}@cnap-hub",
                "seq": _seq(e.updated_at),
                "stamp": e.updated_at,
                "title": e.title,
                "day": e.starts_on,
                "last_day": e.last_day,
                "starts": None,
                "ends": None,
                "place": e.place,
                "details": "\n".join(x for x in (e.time_text, e.summary) if x),
                "url": e.url or fund,
                "kind": "ctr",
            }
        )
    out.sort(key=lambda x: (x["day"], x["starts"] or time(0), x["title"]))
    return out


# -- iCalendar text ---------------------------------------------------------------------------------
def _esc(s):
    return (
        str(s or "")
        .replace("\\", "\\\\")
        .replace(";", "\;")
        .replace(",", "\\,")
        .replace("\r\n", "\n")
        .replace("\n", "\\n")
    )


def _fold(line):
    """Lines over 75 octets continue on the next line after a space (RFC 5545, 3.1)."""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    parts, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > (75 if not parts else 74):
            parts.append(cur.decode("utf-8"))
            cur = b""
        cur += b
    parts.append(cur.decode("utf-8"))
    return "\r\n ".join(parts)


def _utc(d, t):
    return (
        datetime.combine(d, t, tzinfo=CENTRAL)
        .astimezone(ZoneInfo("UTC"))
        .strftime("%Y%m%dT%H%M%SZ")
    )


def ics(today=None):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//CNAP Member Hub//Center calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{_esc(NAME)}",
        "X-WR-TIMEZONE:America/Chicago",
        "X-WR-CALDESC:NeuroSync talks\\, Center events\\, and reporting deadlines from the CNAP Member Hub.",
        "REFRESH-INTERVAL;VALUE=DURATION:PT1H",
        "X-PUBLISHED-TTL:PT1H",
    ]
    for it in items(today):
        stamp = (
            (it["stamp"] or timezone.now()).astimezone(ZoneInfo("UTC")).strftime("%Y%m%dT%H%M%SZ")
        )
        ev = ["BEGIN:VEVENT", f"UID:{it['uid']}", f"DTSTAMP:{stamp}", f"SEQUENCE:{it['seq']}"]
        if it["starts"] is None:
            ev.append(f"DTSTART;VALUE=DATE:{it['day']:%Y%m%d}")
            ev.append(f"DTEND;VALUE=DATE:{it['last_day'] + timedelta(days=1):%Y%m%d}")
            ev.append("TRANSP:TRANSPARENT")
        else:
            ev.append(f"DTSTART:{_utc(it['day'], it['starts'])}")
            if it["ends"]:
                end = _utc(it["last_day"], it["ends"])
            else:
                start = datetime.combine(it["day"], it["starts"])
                end_dt = start + timedelta(hours=1)
                end = _utc(end_dt.date(), end_dt.time())
            ev.append(f"DTEND:{end}")
        ev.append(f"SUMMARY:{_esc(it['title'])}")
        if it["place"]:
            ev.append(f"LOCATION:{_esc(it['place'])}")
        desc = "\n\n".join(x for x in (it["details"], f"More information: {it['url']}") if x)
        ev.append(f"DESCRIPTION:{_esc(desc)}")
        ev.append(f"URL:{it['url']}")
        ev.append("END:VEVENT")
        lines.extend(ev)
    lines.append("END:VCALENDAR")
    return "\r\n".join(_fold(x) for x in lines) + "\r\n"


def as_date(v):
    return v if isinstance(v, date) else date.fromisoformat(str(v))


# -- email-in -----------------------------------------------------------------------------------------
def inbound_key():
    key = getattr(settings, "CALENDAR_INBOUND_KEY", "") or ""
    if key:
        return key
    return hmac.new(
        settings.SECRET_KEY.encode(), b"cnap-calendar-inbound", hashlib.sha256
    ).hexdigest()[:40]


def inbound_key_ok(key):
    return hmac.compare_digest(str(key), inbound_key())


def inbound_path():
    return reverse("calendar_inbound", args=[inbound_key()])
