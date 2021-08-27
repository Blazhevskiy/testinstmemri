from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from customer.models import Customer


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.customer_data = {
            'email': 'some@mail.com',
            'first_name': 'John',
            'last_name': 'Dou',
            'subscription': False,
            'password': 'MySuperStrongPassword1!'
        }

    def test_create_customer(self):
        url = reverse('v1:customer-create')

        self.assertEqual(Customer.objects.count(), 0)
        response = self.client.post(url, data=self.customer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertTrue(Customer.objects.count(), 1)

    def test_create_customer_validation_failed(self):
        url = reverse('v1:customer-create')
        payload = {}

        for k, v in self.customer_data.items():
            payload[k] = v
            response = self.client.post(url, data=payload)

            if payload != self.customer_data:
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            else:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_customer_password_validation(self):
        url = reverse('v1:customer-create')
        wrong_passwords = [
            'asd',  # too short
            'asdqweaa',  # no one digit
            '12345678',  # no letters
            'Abcdefghijklmnopqrstuvwzyx1234567890',  # too long
        ]
        for bad_password in wrong_passwords:
            self.customer_data['password'] = bad_password
            response = self.client.post(url, data=self.customer_data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_languages(self):
        lan_data = {
            'en': {
                'en': 'english',
                'ru': 'russian'
            },
            'ru': {
                'en': 'английский',
                'ru': 'русский'
            }
        }
        url = reverse('v1:management-languages-list')
        for lang_code, languages in lan_data.items():
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE=lang_code)
            self.assertEqual(response.data, languages)
