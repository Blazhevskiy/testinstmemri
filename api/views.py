from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from condo_wiz.utils import get_header_by_name
from api.serializer import EmptySerializer



class ManagementViewSet(viewsets.GenericViewSet):
    """
    The scope of management APIs
    """
    queryset = User.objects.none()
    serializer_class = EmptySerializer
    pagination_class = None

    @action(detail=False, methods=['GET'], permission_classes=(AllowAny,), authentication_classes=())
    def health_check(self, request):
        """
        Return **200 OK** status code and empty response
        """
        return Response()

    @action(
        detail=False,
        methods=['GET'],
        url_path='min_apps_version',
        url_name='min_apps_version',
        permission_classes=(AllowAny,),
        authentication_classes=()
    )
    def minimal_supporting_version(self, request):
        """
        Return minimal supporting version of mobile applications
        """
        platform = get_header_by_name(request, settings.MIN_APP_VERSION_HEADER)
        return Response(data={'version': settings.MOBILE_APP_VERSIONS[platform]})

    @action(
        detail=False,
        methods=['GET'],
        url_path='languages/list',
        url_name='languages-list',
        permission_classes=(AllowAny,),
        authentication_classes=()
    )
    def get_languages(self, request):
        return Response(dict(settings.LANGUAGES))
