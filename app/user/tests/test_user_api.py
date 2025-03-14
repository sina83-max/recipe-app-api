"""
Tests for user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test public feature of the user API."""
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Tests creating user successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'passtest123',
            'name': 'test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists(self):
        """Checks if a user exists with the same email we want to create."""
        payload = {
            'email': 'test@example.com',
            'password': 'passtest123',
            'name': 'test name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Tests if the password is less than 5 characters"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
