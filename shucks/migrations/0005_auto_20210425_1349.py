# Generated by Django 3.2 on 2021-04-25 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shucks', '0004_alter_advert_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='about',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='advert',
            name='company_name',
            field=models.CharField(default='wavegrid', max_length=100),
            preserve_default=False,
        ),
    ]
