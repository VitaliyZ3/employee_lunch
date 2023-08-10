from rest_framework import serializers
from .models import Restaurant, FoodKitchen, Menu, Dish


class FoodKitchenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodKitchen
        fields = "__all__"


class MenuCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class RestaurantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("name", "location", "food_type")
