"""Events by email (MW 2026-11-27).

The CNAP team emails an event to the Hub's inbound address. Postmark posts the email here, and it becomes
a draft on the Calendar page, with its date, time, and place read from the email where they're clear. A
person publishes it with one click, so a misread date never reaches 70 calendars on its own. Only emails
from people who can manage the Hub are accepted.
"""

import re
from datetime import date, time

from django.utils import timezone

MONTHS = {
    m: i
    for i, ms in enumerate(
        [
            ("jan", "january"),
            ("feb", "february"),
            ("mar", "march"),
            ("apr", "april"),
            ("may",),
            ("jun", "june"),
            ("jul", "july"),
            ("aug", "august"),
            ("sep", "sept", "september"),
            ("oct", "october"),
            ("nov", "november"),
            ("dec", "december"),
        ],
        start=1,
    )
    for m in ms
}
_MON = r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sept?(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\.?"
_WORD_DATE = re.compile(_MON + r"\s+(\d{1,2})(?:st|nd|rd|th)?(?:,?\s+(\d{4}))?", re.I)
_NUM_DATE = re.compile(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b")
_DAY_RANGE = re.compile(
    _MON
    + r"\s+(\d{1,2})(?:st|nd|rd|th)?\s*(?:-|–|—|to|through|thru)\s*(\d{1,2})(?:st|nd|rd|th)?"
    + r"(?!\s*(?::|[ap]\.?\s*m\b))(?:,?\s+(\d{4}))?",
    re.I,
)
_ISO_DATE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
_AMPM = r"\s*([ap])\.?\s*m\.?"
_TIME = re.compile(r"\b(\d{1,2})(?::(\d{2}))?(" + _AMPM + r")?", re.I)
_RANGE = re.compile(
    r"\b(\d{1,2})(?::(\d{2}))?(?:"
    + _AMPM
    + r")?\s*(?:-|–|—|to|until)\s*(\d{1,2})(?::(\d{2}))?"
    + _AMPM,
    re.I,
)
_SINGLE = re.compile(r"\b(?:at\s+)?(\d{1,2})(?::(\d{2}))?" + _AMPM, re.I)
_PLACE = re.compile(r"^\s*(?:where|location|place|room)\s*:\s*(.+)$", re.I | re.M)
_URL = re.compile(r"https?://[^\s<>\")\]]+")
_PREFIX = re.compile(r"^\s*((?:re|fw|fwd)\s*:\s*|\[?event\]?\s*:\s*)+", re.I)


def _year_for(month, day, today):
    """No year given: the next time that day comes around."""
    y = today.year
    try:
        d = date(y, month, day)
    except ValueError:
        return None
    return d if d >= today else _safe(y + 1, month, day)


def _safe(y, m, d):
    try:
        return date(y, m, d)
    except ValueError:
        return None


def find_dates(text, today):
    out = []
    for m in _WORD_DATE.finditer(text):
        mon = MONTHS[m.group(1).lower().rstrip(".")]
        day = int(m.group(2))
        d = _safe(int(m.group(3)), mon, day) if m.group(3) else _year_for(mon, day, today)
        if d:
            out.append((m.start(), d))
    for m in _ISO_DATE.finditer(text):
        d = _safe(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if d:
            out.append((m.start(), d))
    for m in _NUM_DATE.finditer(text):
        mon, day = int(m.group(1)), int(m.group(2))
        if m.group(3):
            y = int(m.group(3))
            d = _safe(y + 2000 if y < 100 else y, mon, day)
        else:
            d = _year_for(mon, day, today)
        if d:
            out.append((m.start(), d))
    return [d for _, d in sorted(out)]


def _hm(h, m, ap):
    h, m = int(h), int(m or 0)
    if h > 12 or m > 59:
        return None
    if ap:
        ap = ap.lower()
        if ap == "p" and h != 12:
            h += 12
        if ap == "a" and h == 12:
            h = 0
    return time(h, m)


def find_days(text, today):
    """'March 3-5, 2027' -> (March 3, March 5). Otherwise the first date found, and a second one close after."""
    m = _DAY_RANGE.search(text)
    if m:
        mon = MONTHS[m.group(1).lower().rstrip(".")]
        a, b = int(m.group(2)), int(m.group(3))
        first = _safe(int(m.group(4)), mon, a) if m.group(4) else _year_for(mon, a, today)
        last = _safe(first.year, mon, b) if first else None
        if first and last and last > first:
            return first, last
    dates = find_dates(text, today)
    first = dates[0] if dates else None
    last = None
    if len(dates) > 1 and dates[1] > first and (dates[1] - first).days <= 14:
        last = dates[1]
    return first, last


def find_times(text):
    text = re.sub(r"\bnoon\b", "12 p.m.", text, flags=re.I)
    text = re.sub(r"\bmidnight\b", "12 a.m.", text, flags=re.I)
    m = _RANGE.search(text)
    if m:
        end_ap = m.group(6)
        start_ap = m.group(3) or end_ap
        s, e = _hm(m.group(1), m.group(2), start_ap), _hm(m.group(4), m.group(5), end_ap)
        if s and e and e <= s and not m.group(3) and end_ap.lower() == "p":
            s = _hm(m.group(1), m.group(2), "a")  # "11 to 1 p.m."
        return s, e
    m = _SINGLE.search(text)
    if m:
        return _hm(m.group(1), m.group(2), m.group(3)), None
    return None, None


def parse(subject, body, today=None):
    """Read an emailed event into the fields of a draft."""
    today = today or timezone.localdate()
    title = _PREFIX.sub("", subject or "").strip() or "Event from email"
    text = f"{subject or ''}\n{body or ''}"
    first, last = find_days(text, today)
    starts, ends = find_times(text)
    place = _PLACE.search(body or "")
    url = _URL.search(body or "")
    details = (body or "").strip()
    if len(details) > 2000:
        details = details[:2000].rsplit(" ", 1)[0] + " …"
    return {
        "title": title[:200],
        "day": first or today,
        "end_day": last,
        "starts": starts,
        "ends": ends,
        "place": (place.group(1).strip() if place else "")[:300],
        "url": (url.group(0).rstrip(".,;") if url else "")[:500],
        "details": details,
        "check_date": first is None,
    }
