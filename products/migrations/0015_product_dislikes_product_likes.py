# Generated by Django 4.1.3 on 2023-07-30 06:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0014_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='disliked_products', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_products', to=settings.AUTH_USER_MODEL),
        ),
    ]
