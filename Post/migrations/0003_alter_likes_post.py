# Generated by Django 5.0.3 on 2024-04-02 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0002_rename_post_postx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='Post.postx'),
        ),
    ]
