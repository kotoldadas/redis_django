from django.urls import path
from .views import cache_view


urlpatterns = [path("", cache_view, name="main")]
