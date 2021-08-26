from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    username = models.CharField(_("Username"), max_length=32, blank=True)
    email = models.EmailField(_("Email address"), blank=False, unique=True, help_text=_("Email"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    def save(self, *args, **kwargs):
        self.clean()
        self.username = self.email
        super().save(*args, **kwargs)
