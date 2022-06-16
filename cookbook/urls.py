from django.urls import path
from .views import cache, sync, queued


urlpatterns = [path("", cache), path("sync/", sync), path("queued/", queued)]
