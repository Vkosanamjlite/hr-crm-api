"""
Test for models module
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from core.models import Recipe


class ModelsTestCase(TestCase):
    """
    Test for models
    """

    def test_create_user(self):
        """
        Test creating a user with an email and password.
        """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_with_email_successful(self):
        """ Test creating a new user with an email and password """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', '123654')

    def test_create_superuser(self):
        """
        Test creating a superuser with an email, name, and password
        """
        email = 'superuser@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        # Assert the superuser has been correctly created
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password(password))

    def test_create_recipe(self):
        """" Test creating a new recipe """
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        recipe = Recipe.objects.create(
            user=user,
            title='Test Recipe',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Test Description'

        )
        self.assertEqual(str(recipe), recipe.title)
