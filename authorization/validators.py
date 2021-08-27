from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError


class MaxLengthValidator:
    """
    Validate whether the password is of a maximum length.
    """
    def __init__(self, max_length=32):
        self.max_length = max_length

    def validate(self, password, user=None):
        length_password = len(password)
        if length_password > self.max_length:
            raise ValidationError(
            _(f"Ensure the password has at most {self.max_length} character (it has {length_password})."))

    def get_help_text(self):
        return _(f"Ensure the password has at most {self.max_length} character.")
