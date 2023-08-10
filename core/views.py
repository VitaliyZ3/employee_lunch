from rest_framework import generics
from rest_framework import permissions
from .models import (
    Restaurant,
    FoodKitchen
)
from .serializers import (
    RestaurantCreateSerializer,
    FoodKitchenCreateSerializer
)


class RestaurantCreateView(generics.CreateAPIView):

    serializer_class = RestaurantCreateSerializer
    # permission_classes = [permissions.IsAuthenticated]


class FoodKitchenCreateView(generics.CreateAPIView):

    serializer_class = FoodKitchenCreateSerializer
    # permission_classes = [permissions.IsAuthenticated]
