from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from authorization.auth import RefreshTokenAuthentication
from customer.models import Customer
from exceptions.internal_code_errors import INVALID_CREDENTIALS, USER_INACTIVE
from exceptions.internal_exceptions import AuthInternalError


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        email = data['email']
        password = data['password']

        try:
            customer = authenticate(username=email, password=password)
        except ValidationError:
            customer = None

        if customer:
            if not customer.is_active:
                raise AuthInternalError(USER_INACTIVE)
            data['customer'] = customer
            return data

        raise AuthInternalError(INVALID_CREDENTIALS)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'subscription', 'language_id']


class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=32, help_text=_('First name'))
    last_name = serializers.CharField(required=True, max_length=64, help_text=_('Last name'))
    email = serializers.EmailField(required=True, help_text=_('Email'))
    subscription = serializers.BooleanField(default=False, help_text=_('Subscription'))
    password = serializers.CharField(required=True, help_text=_('Password'))

    def validate_email(self, value):
        if Customer.objects.filter(email=value).exists():
            raise ValidationError(_('Email must be unique'))
        return value

    def validate_password(self, value):
        if not any(symbol.isdigit() for symbol in value):
            raise ValidationError(_('Password must contain at least one digit'))
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Customer(**validated_data)
        user.set_password(password)
        user.save()
        return user


class GetTokensByRefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, help_text=_("User's refresh_token"))

    def validate_refresh_token(self, value):
        try:
            RefreshTokenAuthentication().authenticate_credentials(value)
        except AuthenticationFailed as e:
            raise ValidationError(e)

        return value
