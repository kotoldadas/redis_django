from django.contrib import admin
from .models import Food, Recipe, Ingredient
# Register your models here.

admin.site.register(Food)
admin.site.register(Recipe)
admin.site.register(Ingredient)