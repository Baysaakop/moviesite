# Generated by Django 2.2.3 on 2020-06-03 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0037_series_tomatometer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='cast',
            new_name='maincast',
        ),
        migrations.AddField(
            model_name='movie',
            name='tomatometer',
            field=models.IntegerField(default=0),
        ),
    ]