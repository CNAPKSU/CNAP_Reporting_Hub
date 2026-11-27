# MW 2026-11-25: "Title" instead of "Position title", and the person's roles in the Center (several allowed).

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
            name="center_roles",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="How the person describes their part in CNAP (any of CENTER_ROLES). It does not decide which forms they receive.",
                verbose_name="Roles in the Center",
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
