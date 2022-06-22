import io
from django.shortcuts import HttpResponse, redirect, render
import os

from redis_tutorial.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
)

from django.conf import settings
from .models import Document
import boto3
import zipfile

# AWS_ACCESS_KEY_ID = getattr(settings, "AWS_ACCESS_KEY_ID", "")
# AWS_SECRET_ACCESS_KEY = getattr(settings, "AWS_SECRET_ACCESS_KEY", "")
# AWS_STORAGE_BUCKET_NAME = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "")

# Create your views here.


def image_upload(request):
    if request.method == "POST":
        image_file = request.FILES["image_file"]
        document = Document(upload=image_file)
        document.save()
        image_url = document.upload.url
        return render(request, "upload.html", {"image_url": image_url})

    return render(request, "upload.html")


def download(request):
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    my_bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)
    if request.method == "GET":
        return render(
            request,
            "download.html",
            {
                "folders": set(
                    [
                        os.path.split(obj.key)[0]
                        for obj in my_bucket.objects.all()
                        # if not str(obj.key).startswith("static")
                    ]
                )
            },
        )

    if request.method == "POST":
        # get folder name from request
        folder_name = request.POST.get("folder_name")

        response = HttpResponse(content_type="application/zip")
        with zipfile.ZipFile(response, "w") as zip_file:

            for s3_object in my_bucket.objects.all():
                path, filename = os.path.split(s3_object.key)

                if folder_name == path:
                    # create buffer to append file to zip
                    buffer = io.BytesIO()
                    # download file from s3 to buffer
                    my_bucket.download_fileobj(s3_object.key, buffer)
                    # append buffer to zip
                    zip_file.writestr(filename, buffer.getvalue())

        response["Content-Disposition"] = f"attachment; filename=result.zip"

        return response

    return redirect("main")
