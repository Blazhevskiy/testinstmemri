from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from .auth import RefreshTokenAuthentication


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        email = data["email"]
        password = data["password"]

        try:
            customer = authenticate(username=email, password=password)
        except ValidationError:
            customer = None

        if customer:
            if not customer.is_active:
                raise NotAuthenticated
            data["customer"] = customer
            return data

        raise AuthenticationFailed


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class CreateUserSerializer(serializers.Serializer):
    username_name = serializers.CharField(required=True, max_length=32, help_text=_("Username"))
    email = serializers.EmailField(required=True, help_text=_("Email"))
    password = serializers.CharField(required=True, help_text=_("Password"))

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError(_("Email must be unique"))
        return value

    def validate_password(self, value):
        if not any(symbol.isdigit() for symbol in value):
            raise ValidationError(_("Password must contain at least one digit"))
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        customer = User(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer


class GetTokensByRefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, help_text=_("User's refresh_token"))

    def validate_refresh_token(self, value):
        try:
            RefreshTokenAuthentication().authenticate_credentials(value)
        except AuthenticationFailed as e:
            raise ValidationError(e)

        return value
