# Generated by Django 4.1.3 on 2023-06-21 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='language',
            field=models.CharField(choices=[('MALAYALAM', 'malayalam'), ('ENGLISH', 'english'), ('TAMIL', 'tamil'), ('HINDI', 'hindi')], default='malayalam', max_length=200),
        ),
    ]
