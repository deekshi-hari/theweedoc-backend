from django.db import models
from django.contrib.auth.models import AbstractUser


# class UserType(models.Model):
#     name = models.CharField(max_length=100)

class User(AbstractUser):

    USERTYPE = [
        ('admin', 'ADMIN'),
        ('superadmin', 'SUPERADMIN'),
        ('user', 'USER'),
        ]
    
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    user_type = models.CharField(max_length=50, choices=USERTYPE, default='user')
    profile_pic = models.CharField(max_length=700, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def follow(self, user):
        self.followers.add(user)

    def unfollow(self, user):
        self.followers.remove(user)

    def is_following(self, user):
        return self.followers.filter(pk=user.pk).exists()

    def __str__(self):
        return f"{self.email} -- {self.pk}"
    

class UserOTP(models.Model):
    email = models.EmailField(blank=True)
    phone_number = models.CharField(blank=True, max_length=14)
    otp = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    