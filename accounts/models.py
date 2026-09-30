import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractUser):
    """Email-as-login user. `username` is dropped in favour of `email`."""

    username = None
    email = models.EmailField("email address", unique=True)
    full_name = models.CharField(max_length=120, blank=True)
    is_verified = models.BooleanField(
        default=False,
        help_text="Set once the user confirms the code emailed to them.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.full_name or self.email

    @property
    def display_name(self):
        return self.full_name or self.email.split("@")[0]


class EmailCode(models.Model):
    """Short-lived numeric code emailed to confirm an account or a login."""

    PURPOSE_CHOICES = [
        ("signup", "Account confirmation"),
        ("login", "Login confirmation"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="codes")
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES, default="signup")
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} for {self.user.email} ({self.purpose})"

    @property
    def is_expired(self):
        ttl = getattr(settings, "EMAIL_CODE_TTL_MINUTES", 15)
        return timezone.now() > self.created_at + timedelta(minutes=ttl)

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired

    @classmethod
    def issue(cls, user, purpose="signup"):
        """Invalidate old unused codes, then create a fresh one."""
        cls.objects.filter(user=user, purpose=purpose, is_used=False).update(is_used=True)
        code = f"{random.randint(0, 999999):06d}"
        return cls.objects.create(user=user, code=code, purpose=purpose)
