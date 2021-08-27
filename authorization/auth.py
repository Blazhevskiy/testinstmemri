from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from authorization.models import RefreshToken
from exceptions.internal_code_errors import INVALID_ACCESS_TOKEN, ACCESS_TOKEN_EXPIRED
from exceptions.internal_exceptions import AuthInternalError, USER_INACTIVE, TOKENS_EXPIRED


class AccessTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key, delete_token=True):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthInternalError(INVALID_ACCESS_TOKEN)

        if not token.user.is_active:
            raise AuthInternalError(USER_INACTIVE)

        if (timezone.now() > token.created + timezone.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION)):
            if delete_token:
                try:
                    token.user.auth_token.delete()
                except Token.DoesNotExist:
                    pass

            # Check on expired refresh token
            self._check_refresh_token(token.user)

            raise AuthInternalError(ACCESS_TOKEN_EXPIRED)
        return token.user, token

    def _check_refresh_token(self, user):
        need_re_login = False
        try:
            refresh_token = RefreshToken.objects.get(user=user)
        except RefreshToken.DoesNotExist:
            need_re_login = True

        if not need_re_login:
            if timezone.now() > refresh_token.expired:
                try:
                    user.refresh_token.delete()
                except RefreshToken.DoesNotExist:
                    pass
                need_re_login = True

        if need_re_login:
            raise AuthInternalError(TOKENS_EXPIRED)


class RefreshTokenAuthentication(TokenAuthentication):
    keyword = 'RefreshToken'
    model = RefreshToken

    def authenticate_credentials(self, key):
        user, refresh_token = super().authenticate_credentials(key)
        if timezone.now() > refresh_token.expired:
            try:
                user.refresh_token.delete()
            except RefreshToken.DoesNotExist:
                pass
            raise AuthInternalError(TOKENS_EXPIRED)
        return user, refresh_token


def delete_user_tokens(customer):
    try:
        customer.auth_token.delete()
    except (Token.DoesNotExist, AttributeError):
        pass

    try:
        customer.refresh_token.delete()
    except (RefreshToken.DoesNotExist, AttributeError):
        pass
