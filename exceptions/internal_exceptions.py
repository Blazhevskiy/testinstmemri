import re
import json

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException

from .internal_code_errors import *


class BaseInternalError(APIException):
    """
    Class for internal errors.

    :param inner_code: integer, first three symbols is real http code error,
        and last three give us possibility to create up to 999 internal errors
    :param args: should use for formatting message
    :param kwargs: will appear in response for additional information

        Note:
            For field specification in message use empty braces '{}' or numeric
            braces '{0}, {1}, ...', named braces is not supported because
            kwargs uses for additional information in response.
    """

    _descriptions = {}

    def __init__(self, inner_code, *args, **kwargs):
        assert inner_code in self._descriptions, 'Wrong HTTP error code'

        self.args = args
        self.kwargs = kwargs
        self.error_code = inner_code
        self.status_code = inner_code // 1000
        self._message = None

    @property
    def detail(self):
        if not self._message:
            self._message = {'error_code': self.error_code, 'message': ''}

            message = self._descriptions[self.error_code]
            p = re.compile(r'({{1}(\S*)}{1})')
            if p.search(str(message)):
                message = self._format_error(message)

            self._message['message'] = [force_text(message)]
            for kwarg in self.kwargs:
                self._message[kwarg] = self.kwargs[kwarg]
        return self._message

    def _format_error(self, message):
        try:
            return message.format(*self.args)
        except (KeyError, IndexError, Exception):
            return message

    def __str__(self):
        return json.dumps(self.detail)


class AuthInternalError(BaseInternalError):
    _descriptions = {
        USER_INACTIVE: _('User inactive or deleted'),
        TOKENS_EXPIRED: _('Pair of Tokens are expired'),
        PASSWORD_EXPIRED: _('Your password is expired and should be changed'),
        NO_LOGIN_TOKEN: _('Please obtain a login token first'),
        INVALID_CREDENTIALS: _('Wrong login credentials. Please try again'),
        INVALID_ACCESS_TOKEN: _('Invalid Access token'),
        ACCESS_TOKEN_EXPIRED: _('Access token expired'),
    }


class APIVersionException(BaseInternalError):
    _descriptions = {
        INVALID_VERSION: _('Invalid API version in URL path'),
        UPDATE_REQUIRED: _('Client software update required'),
        INVALID_MIN_APP_VERSION_HEADER: _("Invalid 'platform' header"),
    }
