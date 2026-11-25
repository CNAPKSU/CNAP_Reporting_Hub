# Written by hand (MW 2026-11-24): members can ask to change their own roles from their profile.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reporting", "0013_roster_check"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rostersuggestion",
            name="link",
            field=models.ForeignKey(
                blank=True,
                help_text="Empty when a member asked from their own profile (MW 2026-11-24).",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="suggestions",
                to="reporting.rosterchecklink",
            ),
        ),
        migrations.AlterField(
            model_name="rostersuggestion",
            name="kind",
            field=models.CharField(
                choices=[
                    ("left", "Has left or changed role"),
                    ("new", "Someone new"),
                    ("core_user", "A new core user"),
                    ("other", "Something else"),
                    ("own", "A member asks to change their own roles"),
                ],
                max_length=12,
            ),
        ),
    ]
