# Generated by Django 3.2 on 2021-04-29 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shucks', '0015_auto_20210428_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subcategory',
        ),
        migrations.DeleteModel(
            name='Subcategory',
        ),
    ]