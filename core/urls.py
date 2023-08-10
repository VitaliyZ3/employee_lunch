from django.urls import path
from .views import (
    RestaurantCreateView,
    FoodKitchenCreateView
)
urlpatterns = [
    path("restaurant-create/", RestaurantCreateView.as_view(), name="restaurant_create"),
    path("food-kitcken-create/",FoodKitchenCreateView.as_view(), name="food_kitcken_create")
]