from django.db import models

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="İsim")
    last_name = models.CharField(max_length=30, verbose_name="Soy İsim")
    age = models.IntegerField(verbose_name="Yaş")

    def __str__(self):
        return f"name => {self.first_name} - last name => {self.last_name} - age => {self.age}"
