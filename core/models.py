from django.db import models


class FoodKitchen(models.Model):
    name = models.CharField(max_length=20, verbose_name="Kitchen name")
    description = models.TextField("About cooking type")


class Dish(models.Model):
    name = models.CharField(max_length=20, verbose_name="Dish name")
    description = models.TextField("About dish")


class Menu(models.Model):
    dishes = models.ManyToManyField(
        Dish, related_name="menu", blank=True, verbose_name="Menu dishes"
    )
    uploaded_date = models.DateTimeField(
        auto_now=True, verbose_name="Menu upadated date"
    )


class Restaurant(models.Model):
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
    )


class MenuVotes(models.Model):
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
