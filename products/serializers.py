from rest_framework import serializers
from .models import Product, Genere
from users.models import User


class GenereRetriveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genere
        fields = ['id', 'name']


class CastSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'profile_pic', 'designation', ]


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name']


class ProductRetriveSerializer(serializers.ModelSerializer):
    genere = GenereRetriveSerializer(many=True)
    customer = serializers.SerializerMethodField()
    cast = CastSerializer(many=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    def get_customer(self, obj):
        if obj.customer.first_name=="" and obj.customer.last_name=="":
            return obj.customer.username
        return obj.customer.first_name + ' ' + obj.customer.last_name
    
    def get_like_count(self, obj):
        return obj.likes.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
