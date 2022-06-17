# Generated by Django 4.0.5 on 2022-06-17 07:17

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_groups_customuser_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='custom_user',
        ),
    ]