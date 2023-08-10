from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Restaurant, FoodKitchen, Menu, Dish, MenuVotes
from django.contrib.auth.password_validation import validate_password
from datetime import date


class FoodKitchenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodKitchen
        fields = "__all__"


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ("name", "description")


class MenuCreateSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, write_only=False)
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(), write_only=True
    )

    class Meta:
        model = Menu
        fields = ("restaurant", "dishes", "uploaded_date")

    def create(self, validated_data):
        dishes_data = validated_data.pop("dishes")
        restaurant = validated_data.pop("restaurant")
        today = date.today()

        try:
            menu = Menu.objects.get(restaurant=restaurant, uploaded_date__date=today)
        except Menu.DoesNotExist:
            menu = Menu.objects.create(restaurant=restaurant, **validated_data)

            for dish_data in dishes_data:
                dish, created = Dish.objects.get_or_create(**dish_data)
                menu.dishes.add(dish)
        else:
            menu.dishes.clear()
            for dish_data in dishes_data:
                dish, created = Dish.objects.get_or_create(**dish_data)
                menu.dishes.add(dish)

        restaurant.menu = menu
        restaurant.save()

        return menu


class RestaurantRetrieveSerializer(serializers.ModelSerializer):
    menu = MenuCreateSerializer()

    class Meta:
        model = Restaurant
        fields = "__all__"


class RestaurantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("name", "location", "food_type")


class MenuVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuVotes
        fields = ("menu",)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
