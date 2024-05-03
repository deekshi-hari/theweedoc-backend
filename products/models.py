from django.db import models
from users.models import User
from django.utils import timezone


class Genere(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        "updated_at", auto_now=True, blank=True, null=True
    )


class ProductManagerActive(models.Manager):

    def get_is_active(self):
        return self.filter(status="approved").order_by("-created_at")

    def get_inactive(self):
        return self.filter(is_active=False).order_by("-created_at")


class Languages(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)


class Product(models.Model):
    Language_choice = [
        ("malayalam", "MALAYALAM"),
        ("english", "ENGLISH"),
        ("tamil", "TAMIL"),
        ("hindi", "HINDI"),
    ]

    STATUS = [
        ("approved", "APPROVED"),
        ("rejected", "REJECTED"),
        ("pending", "PENDING"),
    ]

    title = models.CharField(max_length=200, unique=True)
    status = models.CharField(choices=STATUS, max_length=50, default="pending")
    status_reason = models.CharField(max_length=800, blank=True)
    description = models.TextField(blank=True, null=True)
    languages = models.ForeignKey(Languages, on_delete=models.CASCADE)
    image = models.CharField(max_length=500, blank=True)
    video = models.CharField(max_length=500, blank=True)
    duration = models.FloatField(blank=True, null=True)
    genere = models.ManyToManyField(Genere)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name="liked_products", blank=True)
    dislikes = models.ManyToManyField(
        User, related_name="disliked_products", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        "updated_at", auto_now=True, blank=True, null=True
    )
    objects = models.Manager()  # The default manager
    custom_objects = ProductManagerActive()


class CastMember(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cast_member = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cast_member} - {self.product.title} ({self.role})"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class SavedMovies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.recipient.username} - {self.content}"
