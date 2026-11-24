"""Create the first administrator from settings, once (MW 2026-11-24, Render launch).

Reads ADMIN_EMAIL, ADMIN_FIRST_NAME, and ADMIN_LAST_NAME from the environment. Safe to run on every start: an
existing account is left as it is, apart from making sure it holds the Administrator role. No password is set;
the administrator signs in with an emailed sign-in link, or sets a password from that link.
"""

import os

from django.core.management.base import BaseCommand

from apps.accounts.models import ApplicationRole, User, UserRole
from apps.people.models import Person, PersonEmail


class Command(BaseCommand):
    help = "Create the first administrator from ADMIN_EMAIL, ADMIN_FIRST_NAME, ADMIN_LAST_NAME. Safe to repeat."

    def handle(self, *args, **options):
        email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
        first = os.environ.get("ADMIN_FIRST_NAME", "").strip()
        last = os.environ.get("ADMIN_LAST_NAME", "").strip()
        if not (email and first and last):
            self.stdout.write(
                "ensure_admin: ADMIN_EMAIL, ADMIN_FIRST_NAME, and ADMIN_LAST_NAME are not all set; skipped."
            )
            return
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            person = Person.objects.filter(emails__email__iexact=email).first()
            if not person:
                person = Person.objects.create(first_name=first, last_name=last)
                PersonEmail.objects.create(person=person, email=email, is_primary=True)
            username = email.split("@")[0]
            if User.objects.filter(username=username).exists():
                username = email
            user = User.objects.create_user(
                username, email, None, person=person, first_name=first, last_name=last
            )
            user.set_unusable_password()
            user.save(update_fields=["password"])
            self.stdout.write(f"ensure_admin: created {email}.")
        role = ApplicationRole.objects.get(code=ApplicationRole.Code.ADMINISTRATOR)
        UserRole.objects.get_or_create(user=user, role=role, scope_core=None)
        self.stdout.write(f"ensure_admin: {email} is an administrator.")
