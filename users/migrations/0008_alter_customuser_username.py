# Generated by Django 4.0.5 on 2022-06-17 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='Default Users', max_length=100, unique=True, verbose_name='Kullanıcı İsmiii'),
        ),
    ]
