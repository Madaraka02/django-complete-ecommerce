# Generated by Django 3.2 on 2021-04-27 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shucks', '0006_auto_20210426_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
