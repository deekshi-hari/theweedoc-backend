from django.db import models
from users.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Product(models.Model):

    Gener_choice = [ 
        ('COMEDY','comedy'),
        ('ACTION','action'),
        ('DRAMA','drama'),
        ('HORROR','horror'),
      ]

    Language_choice = [
        ('malayalam','MALAYALAM'),
        ('english','ENGLISH'),
        ('tamil','TAMIL'),
        ('hindi','HINDI'),
        ]

    title = models.CharField(max_length=200)
    language = models.CharField(choices=Language_choice, max_length=200, default='malayalam')
    image = CloudinaryField(blank=True, null=True)
    video = CloudinaryField(blank=True, null=True)
    genere = models.CharField(choices=Gener_choice, max_length=200, default='comedy')
    customer = models.ForeignKey(User, on_delete=models.CharField)
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)