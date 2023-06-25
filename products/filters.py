from django_filters import rest_framework as rest_filters
from .models import *
import django_filters

class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = '__all__'