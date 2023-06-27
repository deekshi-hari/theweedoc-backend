from django.db import models
from users.models import User
from django.utils import timezone

class Genere(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True, blank=True, null=True)


class ProductManagerActive(models.Manager):

    def get_is_active(self):
        return self.filter(is_active=True).order_by('-created_at')
    
    def get_inactive(self):
        return self.filter(is_active=False).order_by('-created_at')
    

class Product(models.Model):

    Language_choice = [
        ('malayalam', 'MALAYALAM'),
        ('english', 'ENGLISH'),
        ('tamil', 'TAMIL'),
        ('hindi', 'HINDI'),
        ]

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    language = models.CharField(choices=Language_choice, max_length=200, default='malayalam')
    image = models.CharField(max_length=500, blank=True)
    video = models.CharField(max_length=500, blank=True)
    duration = models.FloatField(blank=True, null=True)
    genere = models.ManyToManyField(Genere)
    customer = models.ForeignKey(User, on_delete=models.CharField)
    age = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True, blank=True, null=True)

    objects = models.Manager()  # The default manager
    custom_objects = ProductManagerActive()