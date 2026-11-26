# MW 2026-11-25: "Title" instead of "Position title", and the person's role in the Center.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0010_persondocument"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="position_title",
            field=models.CharField(blank=True, max_length=200, verbose_name="Title"),
        ),
        migrations.AddField(
            model_name="person",
            name="center_role",
            field=models.CharField(
                blank=True,
                choices=[
                    ("research_project_leader", "Research project leader"),
                    ("pilot_project_leader", "Pilot project leader"),
                    ("mentor", "Mentor"),
                    ("core_director", "Core director"),
                    ("core_senior_advisor", "Core senior advisor"),
                    ("core_scientific_advisor", "Core scientific advisor"),
                    ("center_director", "Center Director"),
                    ("center_associate_director", "Center Associate Director"),
                    ("graduate_student", "Graduate student"),
                    ("core_staff", "Core staff"),
                    ("other", "Other"),
                ],
                help_text="How the person describes their part in CNAP. It does not decide which forms they receive.",
                max_length=40,
                verbose_name="Role in the Center",
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="center_role_other",
            field=models.CharField(
                blank=True,
                help_text="Filled in when the role is Other.",
                max_length=200,
                verbose_name="Role in the Center (other)",
            ),
        ),
    ]
