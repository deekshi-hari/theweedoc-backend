from django.db import models
from django.contrib.auth.models import AbstractUser


# class UserType(models.Model):
#     name = models.CharField(max_length=100)


class User(AbstractUser):

    USERTYPE = [
        ("admin", "ADMIN"),
        ("superadmin", "SUPERADMIN"),
        ("user", "USER"),
    ]

    phone_number = models.CharField(max_length=13, blank=True, null=True)
    user_type = models.CharField(max_length=50, choices=USERTYPE, default="user")
    profile_pic = models.CharField(max_length=700, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    followers = models.ManyToManyField(
        "self", related_name="following", symmetrical=False, blank=True
    )
    dob = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    weblink = models.URLField(blank=True, null=True)

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
    otp = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
