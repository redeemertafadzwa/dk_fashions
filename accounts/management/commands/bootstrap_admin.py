import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create/update the owner superuser from DJANGO_SUPERUSER_* env vars (idempotent)."

    def handle(self, *args, **opts):
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip().lower()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        name = os.environ.get("DJANGO_SUPERUSER_NAME", "DK Owner")

        if not email or not password:
            self.stdout.write(
                "bootstrap_admin: DJANGO_SUPERUSER_EMAIL / _PASSWORD not set — skipping."
            )
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"full_name": name, "is_staff": True,
                      "is_superuser": True, "is_verified": True},
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        if not user.full_name:
            user.full_name = name
        user.set_password(password)
        user.save()

        state = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"bootstrap_admin: {state} superuser {email}"))
