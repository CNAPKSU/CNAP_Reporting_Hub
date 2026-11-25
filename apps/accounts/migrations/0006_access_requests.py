# Access requests (MW 2026-11-24, approved feature): people ask to join; an administrator approves or declines.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_link_requests"),
        ("people", "0010_persondocument"),
    ]

    operations = [
        migrations.CreateModel(
            name="AccessRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("department", models.CharField(blank=True, max_length=200)),
                ("connection", models.CharField(blank=True, max_length=300)),
                ("note", models.TextField(blank=True)),
                ("ip", models.GenericIPAddressField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Waiting for review"),
                            ("approved", "Approved"),
                            ("declined", "Declined"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                ("decided_at", models.DateTimeField(blank=True, null=True)),
                (
                    "decided_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="people.person",
                    ),
                ),
            ],
            options={
                "db_table": "access_requests",
                "ordering": ["-created_at"],
            },
        ),
    ]
