# Generated by Django 2.2.3 on 2020-05-21 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0028_auto_20200521_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='writer',
            field=models.ManyToManyField(related_name='writer', to='movies.Artist'),
        ),
    ]
