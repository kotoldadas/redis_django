# Generated by Django 3.2.6 on 2022-07-06 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(default='default@test.com', max_length=254, verbose_name='email'),
        ),
    ]