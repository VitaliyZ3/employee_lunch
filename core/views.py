from datetime import date
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import F, Count
from rest_framework import permissions
from django.utils import timezone
from .models import Restaurant, Menu, MenuVotes, User
from .serializers import (
    RestaurantCreateSerializer,
    FoodKitchenCreateSerializer,
    MenuCreateSerializer,
    RestaurantRetrieveSerializer,
    MenuVotesSerializer,
    UserSerializer,
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
    """
    Handler for getting restaurant menu for today
    """
    serializer_class = RestaurantRetrieveSerializer

    def get_queryset(self):
        cached_data = cache.get("todays_menu_restaurants")

        if cached_data:
            return cached_data
        today = date.today()
        queryset = Restaurant.objects.filter(menu__uploaded_date__date=today)

        cache.set("todays_menu_restaurants", queryset, 3600)

        return queryset


class RestaurantVotesListView(generics.ListAPIView):
    """
    Handler for getting list of restaurants, their menus and votes
    """
    serializer_class = RestaurantRetrieveSerializer

    def get_queryset(self):
        return Restaurant.objects.annotate(votes_count=F("menu__menuvotes__votes_number"))


class AddVoteView(generics.CreateAPIView):
    """
    Handler for adding votes to the menu
    """
    serializer_class = MenuVotesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        menu_id = request.data.get("menu_id")
        employee = request.user

        try:
            menu = Menu.objects.get(id=menu_id)
        except Menu.DoesNotExist:
            return Response(
                {"detail": "Menu not found"}, status=status.HTTP_404_NOT_FOUND
            )

        menu_vote, created = MenuVotes.objects.get_or_create(menu=menu)

        # checking if user previously add vote to the menu
        if employee not in menu_vote.employees.all():
            menu_vote.employees.add(employee)
            menu_vote.votes_number = menu_vote.employees.count()
            menu_vote.save(update_fields=["votes_number"])
            return Response(
                {"detail": "Vote added successfully"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"detail": "Vote already submitted"}, status=status.HTTP_400_BAD_REQUEST
            )


class CreateUserView(generics.CreateAPIView):
    """
    Handler for creating user/employee
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetMajorityVotedRestaurantView(generics.ListAPIView):
    """
    Handler for getting total best votes menu
    """
    serializer_class = MenuCreateSerializer

    def get_queryset(self):
        today = timezone.now().date()
        start_of_day = timezone.make_aware(
            timezone.datetime.combine(today, timezone.datetime.min.time())
        )
        end_of_day = start_of_day + timezone.timedelta(days=1)

        # Get best object MenuVotes which is the most rated menu
        majority_restaurant_votes = (
            MenuVotes.objects.filter(
                voting_date__gte=start_of_day, voting_date__lt=end_of_day
            )
            .values("menu__restaurant")
            .annotate(votes_count=Count("menu__restaurant"))
            .order_by("-votes_count")
            .first()
        )

        if majority_restaurant_votes:
            majority_restaurant_id = majority_restaurant_votes["menu__restaurant"]

            majority_restaurant = Menu.objects.get(
                restaurant=majority_restaurant_id, uploaded_date__date=today
            )

            return [majority_restaurant]

        return []
