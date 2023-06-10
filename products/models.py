from django.db import models
from users.models import User
from django.utils import timezone

CATEGORY_CHOICES = [
    ('mobile', 'Mobile'),
    ('laptop', 'Laptop'),
    ('tablet', 'Tablet'),
    ('earphone', 'Ear Phone'),
    ('earpods', 'Ear Pods'),
    ('gameing_console', 'Gameing Console'),
]

class Product(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='templates/product_images')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} -- {self.pk}'

    def is_registered_before_two_months(self):
        two_months_ago = timezone.now() - timezone.timedelta(days=60)
        if self.created_at == None:
            return False
        return self.created_at < two_months_ago

    def save(self, *args, **kwargs):
        # Check if the product is registered before two months and make it inactive
        if self.is_registered_before_two_months():
            self.is_active = False
        super(Product, self).save(*args, **kwargs)
