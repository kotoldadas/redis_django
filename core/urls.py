from django.urls import path
from .views import download, image_upload

urlpatterns = [
    path("upload/", image_upload, name="upload"),
    path("download/", download, name="download"),
]
