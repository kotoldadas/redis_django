from django.shortcuts import render
from .services import get_recipes


def cache_view(req):
    recipes = get_recipes()
    context = {"recipes": recipes}
    return render(req, "index.html", context)
