from django.urls import path
from .views import (
    RestaurantCreateView,
    FoodKitchenCreateView,
    MenuCreateView,
    MenuRetrieveUpdateDestroyView,
    TodayMenuRestaurantListView
)
urlpatterns = [
    path("restaurant/", RestaurantCreateView.as_view(), name="restaurant_create"),
    path("food-kitcken/",FoodKitchenCreateView.as_view(), name="food_kitcken_create"),
    path("menu/", MenuCreateView.as_view(), name="menu-list-create"),
    path("menu/<int:pk>/", MenuRetrieveUpdateDestroyView.as_view(), name="menu-retrieve-update-destroy"),
    path("restaurant/<int:pk>/", TodayMenuRestaurantListView.as_view(), name="restaurant-menu-retrieve")
]