from rest_framework import serializers
from .models import Product, Genere, Review
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
    has_liked = serializers.SerializerMethodField()
    has_disliked = serializers.SerializerMethodField()

    def get_customer(self, obj):
        if obj.customer.first_name=="" and obj.customer.last_name=="":
            return obj.customer.username
        return obj.customer.first_name + ' ' + obj.customer.last_name
    
    def get_like_count(self, obj):
        return obj.likes.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()
    
    def get_has_liked(self, obj):
        user = self.context['request'].user
        return obj.likes.filter(pk=user.pk).exists()

    def get_has_disliked(self, obj):
        user = self.context['request'].user
        return obj.dislikes.filter(pk=user.pk).exists()

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    genere = GenereRetriveSerializer(many=True)
    customer = serializers.SerializerMethodField()
    cast = CastSerializer(many=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    has_disliked = serializers.SerializerMethodField()
    is_own_product = serializers.SerializerMethodField()

    def get_customer(self, obj):
        if obj.customer.first_name=="" and obj.customer.last_name=="":
            return obj.customer.username
        return obj.customer.first_name + ' ' + obj.customer.last_name
    
    def get_like_count(self, obj):
        return obj.likes.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()
    
    def get_has_liked(self, obj):
        user = self.context['request'].user
        return obj.likes.filter(pk=user.pk).exists()

    def get_has_disliked(self, obj):
        user = self.context['request'].user
        return obj.dislikes.filter(pk=user.pk).exists()
    
    def get_is_own_product(self, obj):
        user = self.context['request'].user
        if obj.customer == user:
            return True
        return False

    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'