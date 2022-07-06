from django.db import models

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="İsim")
    last_name = models.CharField(max_length=30, verbose_name="Soy İsim")
    email = models.EmailField(
        max_length=254, verbose_name="email", default="default@test.com"
    )
    age = models.IntegerField(verbose_name="Yaş")

    def __str__(self):
        return f"name => {self.first_name}\nlast name => {self.last_name}\nage => {self.age}\nemail => {self.email}"
