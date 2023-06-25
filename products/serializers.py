from rest_framework import serializers
from .models import Product, Genere


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class GenereSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genere
        fields = '__all__'