from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from authorization.models import RefreshToken
from django.contrib.auth.models import User


class AuthenticationTest(APITestCase):

    def test_anonymous_access(self):
        url = reverse('v1:customer-logout')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_customer(self):
        password = 'MyStrongPass1'
        customer = mommy.make(User)
        customer.set_password(password)
        customer.save()

        url = reverse('v1:customer-login')
        response = self.client.post(
            url, data={
                'email': customer.email,
                'password': password,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('access_token'), customer.auth_token.key)
        self.assertEqual(response.data.get('refresh_token'), customer.refresh_token.key)

    def test_logout_authorized_customer(self):
        url = reverse('v1:customer-logout')
        customer = mommy.make(User)
        mommy.make(Token, user=customer)

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {customer.auth_token.key}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        customer.refresh_from_db()
        self.assertIsNone(getattr(customer, 'auth_token', None))
        self.assertIsNone(getattr(customer, 'refresh_token', None))

    def test_get_new_tokens_by_refresh_token(self):
        url = reverse('v1:customer-new_tokens_by_refresh_token')
        customer = mommy.make(User)
        refresh_token = mommy.make(RefreshToken, user=customer)

        response = self.client.post(url, data={'refresh_token': refresh_token.key})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        self.assertEqual(response.data.get('access_token'), customer.auth_token.key)
        self.assertEqual(response.data.get('refresh_token'), customer.refresh_token.key)
        self.assertNotEqual(refresh_token.key, customer.refresh_token.key)

    def test_get_new_tokens_by_refresh_token_wrong_token(self):
        url = reverse('v1:customer-new_tokens_by_refresh_token')
        customer = mommy.make(User)
        refresh_token = mommy.make(RefreshToken, user=customer)

        response = self.client.post(url, data={'refresh_token': refresh_token.key + '1'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
