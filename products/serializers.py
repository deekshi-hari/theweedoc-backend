from rest_framework import serializers
from .models import Product, Genere
from users.models import User


class GenereRetriveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genere
        fields = ['id', 'name']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name']


class ProductRetriveSerializer(serializers.ModelSerializer):
    genere = GenereRetriveSerializer(many=True)
    customer = serializers.SerializerMethodField()

    def get_customer(self, obj):
        if obj.customer.first_name=="" and obj.customer.last_name=="":
            return obj.customer.username
        return obj.customer.first_name + ' ' + obj.customer.last_name

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'