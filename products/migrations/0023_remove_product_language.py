# Generated by Django 4.1.3 on 2024-05-03 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_product_languages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='language',
        ),
    ]
