from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'language', 'image', 'video', 'genere', 'customer', 'is_active', 'created_at')