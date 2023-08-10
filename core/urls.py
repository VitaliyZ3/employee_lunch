from django.urls import path
from .views import (
    RestaurantCreateView,
    FoodKitchenCreateView,
    MenuCreateView,
    MenuRetrieveUpdateDestroyView,
    TodayMenuRestaurantListView,
    CreateUserView,
    AddVoteView,
    RestaurantVotesListView,
    GetMajorityVotedRestaurantView
)


urlpatterns = [
    path("restaurant/", RestaurantCreateView.as_view(), name="restaurant_create"),
    path("food-kitcken/",FoodKitchenCreateView.as_view(), name="food_kitcken_create"),
    path("menu/", MenuCreateView.as_view(), name="menu_list_create"),
    path("menu/<int:pk>/", MenuRetrieveUpdateDestroyView.as_view(), name="menu_retrieve_update_destroy"),
    path("restaurant/<int:pk>/", TodayMenuRestaurantListView.as_view(), name="restaurant_menu_retrieve"),
    path("create-employee/", CreateUserView.as_view(), name="create_employee"),
    path("restaurant-vote-list/", RestaurantVotesListView.as_view(), name="restaurant_vote_list"),
    path("add-vote/", AddVoteView.as_view(), name="add_vote"),
    path('majority-voted-restaurant/', GetMajorityVotedRestaurantView.as_view(), name='majority-voted-restaurant'),
]