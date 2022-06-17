# Generated by Django 4.0.5 on 2022-06-17 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='id',
        ),
        migrations.RemoveField(
            model_name='task',
            name='taks_id',
        ),
        migrations.AddField(
            model_name='task',
            name='task_id',
            field=models.CharField(default='-1', max_length=100, primary_key=True, serialize=False, unique=True, verbose_name='Görev ID'),
        ),
    ]