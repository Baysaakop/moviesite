# Generated by Django 2.2.3 on 2020-06-16 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0050_auto_20200615_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
