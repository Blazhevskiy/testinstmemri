import os
import binascii

from django.db import models
from django.conf import settings
from django.utils import timezone

from customer.models import Customer


def set_refresh_token_time_expiration():
    return timezone.now() + timezone.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRATION)


class RefreshToken(models.Model):
    """
    The refresh token model.
    """

    key = models.CharField("Key", max_length=40, primary_key=True, help_text='Refresh token')
    user = models.OneToOneField(
        Customer,
        unique=True,
        verbose_name="Customer",
        related_name='refresh_token',
        on_delete=models.CASCADE,
        help_text='ID of user'
    )
    expired = models.DateTimeField(
        default=set_refresh_token_time_expiration,
        help_text='Expired datetime'
    )

    class Meta:
        verbose_name = "Refresh Token"
        verbose_name_plural = "Refresh Tokens"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(RefreshToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return '{}'.format(self.key)
