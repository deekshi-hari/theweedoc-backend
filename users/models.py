from django.db import models
from django.contrib.auth.models import AbstractUser


# class UserType(models.Model):
#     name = models.CharField(max_length=100)

class User(AbstractUser):
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f"{self.email} -- {self.pk}"
    

class UserOTP(models.Model):
    email = models.EmailField(blank=True)
    phone_number = models.CharField(blank=True, max_length=14)
    otp = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    