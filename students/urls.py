from django.urls import path
from .views import index, other, test


urlpatterns = [path("", index, name="students"), path("test/", test, name="test"), path("other/", other, name="other") ]
