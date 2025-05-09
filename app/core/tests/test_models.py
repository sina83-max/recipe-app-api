"""
Tests for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from .. import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    """Test models"""

    def test_user_with_email_successful(self):
        """Test creating a user with email is successful."""
        email = "test@example.com"
        password = 'test123pass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Testing if the new user email is normalized."""

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email,
                password='sample123'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Tests creating a new user without email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Tests creating new superuser"""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='sample123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Tests creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='pass123'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='sample recipe title',
            time_minutes=5,
            price=Decimal('5.50'),
            description='sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful,"""
        user = create_user()
        tag = models.Tag.objects.create(
            user=user,
            name="Sample name for tag"
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Tests creating an ingredient is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient name'
        )

        self.assertEqual(str(ingredient), ingredient.name)
