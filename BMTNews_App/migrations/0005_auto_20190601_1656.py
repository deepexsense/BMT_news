# Generated by Django 2.2.1 on 2019-06-01 13:56

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BMTNews_App', '0004_auto_20190601_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news_img',
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
    ]