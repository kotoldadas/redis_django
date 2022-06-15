from django.shortcuts import render
from django.http import HttpRequest
from .services import get_recipes


def index(req: HttpRequest):
    context = {"recipes": get_recipes()}
    return render(req, "index.html", context)
