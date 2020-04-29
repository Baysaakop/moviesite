# Generated by Django 2.2.3 on 2020-04-29 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_movierating_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followed_artists',
            field=models.ManyToManyField(blank=True, null=True, to='movies.Staff'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='liked_movies',
            field=models.ManyToManyField(blank=True, null=True, related_name='liked_movies', to='movies.Movie'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='watchedlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchedlist', to='movies.Movie'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlist', to='movies.Movie'),
        ),
    ]