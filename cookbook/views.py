from django.shortcuts import render
from django.http import HttpRequest
from .services import get_recipes, tmp
import django_rq


def cache(req: HttpRequest):
    context = {"recipes": get_recipes()}
    return render(req, "index.html", context)


def sync(req: HttpRequest):
    tmp()
    return render(req, "tmp.html")


def queued(req: HttpRequest):
    django_rq.enqueue(tmp)
    return render(req, "tmp.html")
