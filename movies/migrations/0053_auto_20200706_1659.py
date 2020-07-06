# Generated by Django 2.2.3 on 2020-07-06 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0052_auto_20200706_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='trailervideo',
        ),
        migrations.RemoveField(
            model_name='series',
            name='trailervideo',
        ),
        migrations.AlterField(
            model_name='movie',
            name='trailer',
            field=models.FileField(blank=True, null=True, upload_to='movies/trailers/'),
        ),
        migrations.AlterField(
            model_name='series',
            name='trailer',
            field=models.FileField(blank=True, null=True, upload_to='movies/trailers/'),
        ),
    ]
