from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .manager import CustomUserManager

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Email", unique=True, default="text@text.com"
    )
    channel_name = models.CharField(
        blank=True, null=True, verbose_name="kanal ismi", max_length=50
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        db_table = "custom_user"

    def __str__(self):
        return self.email  # type: ignore


class Task(models.Model):
    task_id = models.CharField(
        verbose_name="Görev ID",
        max_length=100,
        primary_key=True,
        unique=True,
        default="-1",
    )

    class StatusChoices(models.TextChoices):
        ON_PROGRESS = "ONP", "On Progress"
        FINISHED = "FNS", "Finished"

    status = models.CharField(
        verbose_name="Görev Durumu",
        choices=StatusChoices.choices,
        max_length=3,
        default=StatusChoices.ON_PROGRESS,
    )
    started = models.DateTimeField(
        auto_now_add=True, verbose_name="Görev Başlama Zamanı"
    )

    def __str__(self):
        return f"id => {self.task_id} - status => {self.status} - started => {self.started}"
