from django.contrib import admin
from .models import Product, Genere, Review, SavedMovies

admin.site.register(Product)
admin.site.register(Genere)
admin.site.register(Review)
admin.site.register(SavedMovies)

