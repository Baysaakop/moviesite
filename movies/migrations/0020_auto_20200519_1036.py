# Generated by Django 2.2.3 on 2020-05-19 02:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0019_movie_score'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Staff',
            new_name='Artist',
        ),
    ]
