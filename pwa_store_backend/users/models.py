from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, OneToOneField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class UserSetting(models.Model):
    LIGHT = 'light'
    DARK = 'dark'
    MODES = [
        (LIGHT, 'Light'),
        (DARK, 'dark'),
    ]
    mode = CharField(
        max_length=20,
        choices=MODES,
        default=LIGHT,
    )

    def __str__(self):
        return self.mode


class User(AbstractUser):
    """Default user for pwa-store-backend."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    modes = OneToOneField(UserSetting, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
