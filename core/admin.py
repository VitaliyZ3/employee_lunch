from django.contrib import admin
from .models import Menu, Restaurant, MenuVotes
# Register your models here.

admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(MenuVotes)