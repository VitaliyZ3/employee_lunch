from datetime import date
from rest_framework import generics
from django.core.cache import cache
from rest_framework import permissions
from .models import (
    Restaurant,
    FoodKitchen,
    Menu
)
from .serializers import (
    RestaurantCreateSerializer,
    FoodKitchenCreateSerializer,
    MenuCreateSerializer,
    RestaurantRetrieveSerializer
)


class RestaurantCreateView(generics.CreateAPIView):

    serializer_class = RestaurantCreateSerializer
    # permission_classes = [permissions.IsAuthenticated]


class FoodKitchenCreateView(generics.CreateAPIView):

    serializer_class = FoodKitchenCreateSerializer
    # permission_classes = [permissions.IsAuthenticated]


class MenuCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuCreateSerializer


class MenuRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuCreateSerializer


class RestaurantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = Restaurant


class TodayMenuRestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantRetrieveSerializer

    def get_queryset(self):
        cached_data = cache.get("todays_menu_restaurants")

        if cached_data:
            return cached_data
        today = date.today()
        queryset = Restaurant.objects.filter(menu__uploaded_date__date=today)

        cache.set("todays_menu_restaurants", queryset, 3600)

        return queryset
