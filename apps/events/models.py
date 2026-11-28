"""The Center calendar (MW 2026-11-27).

Center events the CNAP team adds by hand or by email. With NeuroSync talks, reporting due dates, and
funding events, they make up the calendar feed members subscribe to, so new and changed dates appear in
their own Outlook or Google calendar on their own.
"""

import uuid

from django.conf import settings
from django.db import models

from apps.common.models import TimestampedModel


class CenterEvent(TimestampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft, not on the calendar yet"
        PUBLISHED = "published", "On the calendar"
        CANCELLED = "cancelled", "Cancelled"

    class Source(models.TextChoices):
        FORM = "form", "Added on the Calendar page"
        EMAIL = "email", "Sent in by email"

    title = models.CharField(max_length=200)
    day = models.DateField(help_text="The first day.")
    end_day = models.DateField(
        null=True, blank=True, help_text="The last day, for an event over several days."
    )
    starts = models.TimeField(null=True, blank=True, help_text="Leave blank for an all-day event.")
    ends = models.TimeField(null=True, blank=True)
    place = models.CharField(max_length=300, blank=True)
    details = models.TextField(blank=True)
    url = models.URLField(
        "More information",
        max_length=500,
        blank=True,
        help_text="Where people click through for the details. Blank: the Events page.",
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PUBLISHED)
    # A fixed identity, so a subscribed calendar updates this event instead of adding a copy.
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    source = models.CharField(max_length=6, choices=Source.choices, default=Source.FORM)
    email_from = models.EmailField(blank=True)
    email_subject = models.CharField(max_length=300, blank=True)
    email_body = models.TextField(blank=True)
    check_date = models.BooleanField(
        default=False, help_text="The email didn't name a clear date, so the day is a placeholder."
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    class Meta:
        db_table = "center_events"
        ordering = ["day", "starts", "title"]

    def __str__(self):
        return f"{self.title} ({self.day:%B %-d, %Y})"

    @property
    def last_day(self):
        return self.end_day or self.day

    @property
    def all_day(self):
        return self.starts is None
