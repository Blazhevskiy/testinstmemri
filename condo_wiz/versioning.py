from rest_framework.versioning import NamespaceVersioning
from rest_framework.exceptions import NotFound

from exceptions.internal_exceptions import APIVersionException, INVALID_VERSION


class CustomVersioning(NamespaceVersioning):
    def determine_version(self, request, *args, **kwargs):
        try:
            super().determine_version(request, *args, **kwargs)
        except NotFound:
            raise APIVersionException(INVALID_VERSION)
