# Generated by Django 2.2.3 on 2020-05-27 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0032_series_runningtime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='cast',
        ),
        migrations.AddField(
            model_name='series',
            name='maincast',
            field=models.ManyToManyField(related_name='seriesmaincast', to='movies.Artist'),
        ),
    ]
