# Generated by Django 5.1.9 on 2025-05-16 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='is_available',
        ),
    ]
