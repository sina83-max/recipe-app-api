"""
Tests for tag API
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


def detail_url(tag_id):
    return reverse("recipe:tag-detail", args=[tag_id])


def create_user(email='test@example.com', password='testpass123'):
    """Create and return a user"""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagsApiTests(TestCase):
    """Tests auth is required for retrieving tags."""

    def SetUp(self):
        self.client = APIClient()

    def test_auth_is_required(self):
        """Tests auth is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Tests authenticated API requests"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def retrieve_tags(self):
        """Tests retrieving a list of tags"""
        Tag.objects.create(
            user=self.user,
            name="Vegan"
        )
        Tag.objects.create(
            user=self.user,
            name='Dessert'
        )

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Retrieve tags for the authenticated user"""
        user2 = create_user(
            email="test2@example.com",
            password='pass123',
        )
        Tag.objects.create(
            user=user2,
            name='dinner'
        )
        tag = Tag.objects.create(
            user=self.user,
            name="ice cream"
        )

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_updating_tags(self):
        """Tests updating tags is successful."""
        tag = Tag.objects.create(
            user=self.user,
            name="Sohan"
        )
        payload = {
            "name": "Gaz"
        }

        url = detail_url(tag.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_deleting_tag(self):
        """Deleting exisiting tag"""
        tag = Tag.objects.create(
            user=self.user,
            name="After lunch"
        )

        url = detail_url(tag.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())
