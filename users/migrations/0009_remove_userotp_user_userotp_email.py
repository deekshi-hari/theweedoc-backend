# Generated by Django 4.1.3 on 2023-08-19 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_userotp_email_remove_userotp_phone_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userotp',
            name='user',
        ),
        migrations.AddField(
            model_name='userotp',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
