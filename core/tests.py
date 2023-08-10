from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Restaurant, FoodKitchen, Dish, Menu
from django.test import TestCase
from .serializers import RestaurantCreateSerializer


# Model tests
class RestaurantModelTest(TestCase):
    """
    Test case for restaurant model
    """

    def setUp(self):
        food_type = FoodKitchen.objects.create(name="Some Food Type")
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant", food_type=food_type
        )

    def test_name_label(self):
        field_label = self.restaurant._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Restaurant name")

    def test_name_max_length(self):
        max_length = self.restaurant._meta.get_field("name").max_length
        self.assertEqual(max_length, 20)

    def test_object_name_is_name(self):
        expected_object_name = self.restaurant.name
        self.assertEqual(str(self.restaurant), expected_object_name)


# View Test
class MenuViewTest(TestCase):
    """
    Test case for testing 200 response menu-list/ endpoint
    """

    def setUp(self):
        self.client = APIClient()
        self.dish = Dish.objects.create(
            name="Test Dish", description="Some description"
        )
        self.menu = Menu.objects.create()
        self.menu.dishes.add(self.dish)

    def test_retrieve_menu(self):
        response = self.client.get(
            reverse("menu_retrieve_update_destroy", args=[self.menu.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_menu(self):
        response = self.client.delete(
            reverse("menu_retrieve_update_destroy", args=[self.menu.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RestaurantCreateSerializerTest(TestCase):
    """
    Test case for validation RestaurantCreateSerializer
    """

    def setUp(self):
        self.food_type = FoodKitchen.objects.create(name="Some Food Type")
        self.valid_data = {
            "name": "Test Restaurant",
            "food_type": 1,
            "location": "Kyiv",
        }
        self.serializer = RestaurantCreateSerializer(data=self.valid_data)

    def test_serializer_withinvalid_data(self):
        invalid_data = {"name": "Test Restaurant", "food_type": 0}
        serializer = RestaurantCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_with_valid_data(self):
        self.assertTrue(self.serializer.is_valid())
