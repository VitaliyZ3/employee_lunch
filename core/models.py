from django.db import models
from django.contrib.auth.models import User


class FoodKitchen(models.Model):
    """
    Model that represent Categories of restaurant
    """

    name = models.CharField(max_length=20, verbose_name="Kitchen name")
    description = models.TextField("About cooking type")


class Dish(models.Model):
    """
    Model that represent dishes
    """

    name = models.CharField(max_length=20, verbose_name="Dish name")
    description = models.TextField("About dish")


class Menu(models.Model):
    """
    Model that represent restaurant one day menu
    """

    dishes = models.ManyToManyField(
        Dish, related_name="menu", blank=True, verbose_name="Menu dishes"
    )
    uploaded_date = models.DateTimeField(
        auto_now=True, verbose_name="Menu upadated date"
    )


class Restaurant(models.Model):
    """
    Model that represent restaurant
    """

    name = models.CharField(max_length=20, verbose_name="Restaurant name")
    location = models.CharField(max_length=254, verbose_name="Restaurant address")
    food_type = models.ForeignKey(
        FoodKitchen, related_name="restaurant", on_delete=models.DO_NOTHING, null=False
    )
    menu = models.ForeignKey(
        Menu,
        related_name="restaurant",
        blank=True,
        null=True,
        verbose_name="Restaurant menu",
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.name


class MenuVotes(models.Model):
    """
    Model that represent total menu votes
    """

    menu = models.ForeignKey(
        Menu,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Voting menu",
    )
    votes_number = models.IntegerField(
        blank=True, null=True, verbose_name="Employee voting count"
    )
    voting_date = models.DateTimeField(auto_now=True, verbose_name="Voting date")
    employees = models.ManyToManyField(
        User,
        related_name="menu_votes",
        through="EmployeeVotes",
        blank=True,
        verbose_name="employee who votes",
    )


class EmployeeVotes(models.Model):
    """
    Many-to-Many model for ranking menus
    """

    menu_vote = models.ForeignKey(
        MenuVotes, on_delete=models.CASCADE, related_name="employeevotes"
    )
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="employeevotes"
    )
