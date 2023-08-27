from django.db import models
from users.models import User

# Create your models here.

class Advertisement(models.Model):
    STATUS = [
        ('approved', 'APPROVED'),
        ('rejected', 'REJECTED'),
        ('pending', 'PENDING'),
    ]
    title = models.CharField(max_length=200, unique=True)
    status = models.CharField(choices=STATUS, max_length=50, default='pending')
    description = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=20, blank=True)
    image = models.CharField(max_length=500, blank=True)
    video = models.CharField(max_length=500, blank=True)
    key_words = models.CharField(max_length=500, blank=True)
    duration = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    status_review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True, blank=True, null=True)
