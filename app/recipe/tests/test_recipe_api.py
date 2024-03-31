"""
Test recipe
"""

from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from ..serializers import (
    RecipeSerializer,
    RecipeDetailsSerializer,
)

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """ Return recipe details URL """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    """ Test recipe creation  """
    defaults = {
        'title': 'Test Recipe',
        'description': 'Test Recipe',
        'price': Decimal('5.24'),
        'time_minutes': 22,
        'link': 'https://www.example.com/recipe.pdf',
    }
    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


def create_user(**params):
    """ Test user creation  """
    return get_user_model().objects.create_user(**params)


class RecipeApiTests(TestCase):
    """ Test recipe API request """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test that login is required for retrieving recipe """
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """ Test private recipe API request """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@sample.com', password='test123456')
        # self.user = get_user_model().objects.create_user(
        #     email='test@test.com',
        #     password='testpass'
        # )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """ Test retrieving list of recipes """
        create_recipe(user=self.user)
        create_recipe(user=self.user,
                      title='new recipe',
                      description='sample 2')
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """" Test retrieving recipes for authenticated user """
        user2 = create_user(email='other@example.com', password='test123')
        create_recipe(user=user2,
                      title='other recipe user2',
                      description='sample 3')
        create_recipe(user=user2,
                      title='other recipe user2',
                      description='sample 4')
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_details(self):
        """ Test retrieving recipe details """
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailsSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """ Test creating a new recipe  """
        payload = {
            'title': 'Sample recipe title',
            'time_minutes': 30,
            'price': Decimal('50.29'),
        }
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update_recipe(self):
        """ Test updating """
        original_link = 'https://www.hackerrank.com/recipes.pdf'
        recipe = create_recipe(
            user=self.user,
            title='Sample recipe title',
            link=original_link,
        )
        payload = {
            'title': 'Sample recipe title2'
        }
        url = detail_url(recipe.id)
        self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_update_recipe(self):
        """ Test updating recipe """
        recipe = create_recipe(
            user=self.user,
            title='Sample recipe',
            link='https://www.hackerrank.com/recipes.pdf',
            description='Sample recipe description',
        )
        payload = {
            'title': 'Sample recipe3',
            'link': 'https://www.hackerrank.com/recipes-nre.pdf',
            'description': 'Sample recipe description new',
            'time_minutes': 10,
            'price': Decimal('2.28'),

        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_return_error(self):
        """ Test updating user with invalid details """
        new_user = create_user(
            email='sam@am.com',
            password='test123'
        )
        recipe = create_recipe(user=self.user)
        payload = {
            'user': new_user.id,
        }
        url = detail_url(recipe.id)
        self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """ Test deleting recipe """
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_users_recipe_error(self):
        """ Test deleting other users recipe error """
        new_user = create_user(email='sam@am.com', password='test123a')
        recipe = create_recipe(user=new_user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
