from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Customer(AbstractUser):
    first_name = models.CharField(_('First name'), max_length=32, blank=True)
    last_name = models.CharField(_('Last name'), max_length=64, blank=True)
    email = models.EmailField(_('Email address'), blank=False, unique=True, help_text=_('Email'))
    subscription = models.BooleanField(_('Subscription'), default=False, help_text=_('Subscription'))
    language_id = models.CharField(choices=settings.LANGUAGES, max_length=2, help_text=_('Language'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def save(self, *args, **kwargs):
        self.clean()
        self.username = self.email
        super().save(*args, **kwargs)
