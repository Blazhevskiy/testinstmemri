from datetime import timedelta

from django.contrib.auth import login, logout
from django.db import transaction
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authorization.auth import delete_user_tokens
from authorization.models import RefreshToken
from customer.models import Customer
from customer.serializer import (
    CustomerSerializer, LoginSerializer, CreateUserSerializer,
    GetTokensByRefreshTokenSerializer,
)

from django.utils.translation import ugettext_lazy as _

class CustomerViewSet(viewsets.GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_value_regex = "[0-9]+"

    @action(
        detail=False,
        methods=["POST"],
        serializer_class=LoginSerializer,
        permission_classes=(AllowAny,),
        authentication_classes=(),
        url_path='user/auth',
        url_name='login'
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        customer = data["customer"]

        response_data = self.do_login(request, customer)
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['POST'],
        serializer_class=GetTokensByRefreshTokenSerializer,
        permission_classes=(AllowAny,),
        authentication_classes=(),
        url_path='application/refresh_token',
        url_name='new_tokens_by_refresh_token',
    )
    def get_new_tokens_by_refresh_token(self, request):
        """
        Get new pair of tokens by RefreshToken
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token_key = serializer.validated_data.get('refresh_token')
        refresh_token = RefreshToken.objects.get(key=refresh_token_key)
        customer = refresh_token.user
        response_data = self.create_tokens(customer)
        return Response(data=response_data, status=status.HTTP_200_OK)

    def do_login(self, request, customer):
        """
        Login user and create new pair of tokens
        """
        login(request, customer)
        return self.create_tokens(customer)

    def create_tokens(self, customer):
        """
        Function that creates new pair of tokens
        """
        with transaction.atomic():
            delete_user_tokens(customer)

            access_token = Token.objects.create(user=customer)
            refresh_token = RefreshToken.objects.create(user=customer)

        data = {
            "access_token": access_token.key,
            'access_expiration_date': (access_token.created + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION)),
            "refresh_token": refresh_token.key,
            "refresh_expiration_date": refresh_token.expired,
        }
        return data

    @action(
        detail=False,
        methods=['POST'],
        url_path='user/create',
        url_name='create',
        serializer_class=CreateUserSerializer,
        authentication_classes=(),
        permission_classes=(AllowAny,),
    )
    def create_customer(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            customer = serializer.save()
            response_data = self.do_login(request, customer)

        return Response(data=response_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'], url_path='user/logout', url_name='logout')
    def logout(self, request):
        """Logout Customer and remove tokens"""
        customer = request.user
        delete_user_tokens(customer)
        logout(request)

        return Response(data={"success": _("Successfully logged out")})
