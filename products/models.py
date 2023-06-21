from django.db import models
from users.models import User
from django.utils import timezone


class Product(models.Model):

    Gener_choice = [ 
        ('comedy', 'COMEDY'),
        ('action', 'ACTION'),
        ('drama', 'DRAMA'),
        ('horror', 'HORROR'),
      ]

    Language_choice = [
        ('malayalam', 'MALAYALAM'),
        ('english', 'ENGLISH'),
        ('tamil', 'TAMIL'),
        ('hindi', 'HINDI'),
        ]

    title = models.CharField(max_length=200, unique=True)
    language = models.CharField(choices=Language_choice, max_length=200, default='malayalam')
    image = models.CharField(max_length=500, blank=True)
    video = models.CharField(max_length=500, blank=True)
    genere = models.CharField(choices=Gener_choice, max_length=200, default='comedy')
    customer = models.ForeignKey(User, on_delete=models.CharField)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)