"""Create the first administrator from settings, once (MW 2026-11-24, Render launch).

Reads ADMIN_EMAIL, ADMIN_FIRST_NAME, and ADMIN_LAST_NAME from the environment. Safe to run on every start: an
existing account is left as it is, apart from making sure it holds the Administrator role.

Administrators never sign in by emailed link (apps/accounts/signin.py), so the first one needs a password: set
ADMIN_PASSWORD once, sign in, change it under Change password, then delete ADMIN_PASSWORD from the host. The
password is only ever set on an account that has no usable password yet, so a later start never overwrites one.
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
        password = os.environ.get("ADMIN_PASSWORD", "")
        if password and not user.has_usable_password():
            user.set_password(password)
            user.save(update_fields=["password"])
            self.stdout.write(f"ensure_admin: set the first password for {email}.")
        role = ApplicationRole.objects.get(code=ApplicationRole.Code.ADMINISTRATOR)
        UserRole.objects.get_or_create(user=user, role=role, scope_core=None)
        self.stdout.write(f"ensure_admin: {email} is an administrator.")
