# Generated by Django 5.0.6 on 2024-06-13 10:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0004_likes_liked'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='likes',
            unique_together={('profile', 'post')},
        ),
    ]
