from rest_framework import serializers
from .models import Product, Genere
from users.models import User


class GenereRetriveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genere
        fields = ['id', 'name']


# class CustomerSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['name']


class ProductRetriveSerializer(serializers.ModelSerializer):
    genere = GenereRetriveSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'