import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from apps.users.manager import CustomUserManager


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    Includes automatic created_at and updated_at timestamps.
    """

    email = models.EmailField(unique=True)
    username = None

    # Make email the login field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
