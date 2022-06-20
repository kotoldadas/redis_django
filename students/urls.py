from django.urls import path
from .views import index, result, test


urlpatterns = [
    path("", index, name="students"),
    path("test/", test, name="test"),
    path("result/", result, name="other"),
]
