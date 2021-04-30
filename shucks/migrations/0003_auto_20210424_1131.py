# Generated by Django 3.2 on 2021-04-24 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shucks', '0002_auto_20210423_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='static/images')),
                ('description', models.CharField(max_length=400)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to='static/images'),
        ),
    ]