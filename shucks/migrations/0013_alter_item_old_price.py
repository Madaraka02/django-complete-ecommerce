# Generated by Django 3.2 on 2021-04-27 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shucks', '0012_alter_item_old_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
