import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CenterEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=200)),
                ("day", models.DateField(help_text="The first day.")),
                ("end_day", models.DateField(blank=True, help_text="The last day, for an event over several days.", null=True)),
                ("starts", models.TimeField(blank=True, help_text="Leave blank for an all-day event.", null=True)),
                ("ends", models.TimeField(blank=True, null=True)),
                ("place", models.CharField(blank=True, max_length=300)),
                ("details", models.TextField(blank=True)),
                ("url", models.URLField(blank=True, help_text="Where people click through for the details. Blank: the Events page.", max_length=500, verbose_name="More information")),
                ("status", models.CharField(choices=[("draft", "Draft, not on the calendar yet"), ("published", "On the calendar"), ("cancelled", "Cancelled")], default="published", max_length=10)),
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("source", models.CharField(choices=[("form", "Added on the Calendar page"), ("email", "Sent in by email")], default="form", max_length=6)),
                ("email_from", models.EmailField(blank=True, max_length=254)),
                ("email_subject", models.CharField(blank=True, max_length=300)),
                ("email_body", models.TextField(blank=True)),
                ("check_date", models.BooleanField(default=False, help_text="The email didn't name a clear date, so the day is a placeholder.")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to=settings.AUTH_USER_MODEL)),
            ],
            options={"db_table": "center_events", "ordering": ["day", "starts", "title"]},
        ),
    ]
