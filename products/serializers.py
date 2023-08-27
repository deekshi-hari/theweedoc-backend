from rest_framework import serializers
from .models import Product, Genere, Review, CastMember, SavedMovies
from users.models import User


class GenereRetriveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genere
        fields = ['id', 'name']


# class CustomerDetailSerializer(serializers.ModelSerializer):
#     followers_count = serializers.SerializerMethodField()
#     following_count = serializers.SerializerMethodField()
#     is_following = serializers.SerializerMethodField()

#     # def get_is_following(self, obj):
#     #     if self.context['request'].user.is_authenticated:
#     #         followers_subquery = self.context['followers_subquery_list']
#     #         if obj.id in followers_subquery:
#     #             return True
#     #         return False
#     #     return False

#     # def get_followers_count(self, obj):
#     #     return obj.followers.count()

#     # def get_following_count(self, obj):
#     #     return obj.following.count()

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'designation', 'profile_pic', 
#                   'followers_count', 'following_count', 'is_following']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'designation', 'profile_pic']


class CastSerializer(serializers.ModelSerializer):

    class Meta:
        model = CastMember
        fields = '__all__'


class CastRetriveSerializer(serializers.ModelSerializer):
    cast_member = CustomerSerializer()

    class Meta:
        model = CastMember
        fields = '__all__'


class ProductRetriveSerializer(serializers.ModelSerializer):
    genere = GenereRetriveSerializer(many=True)
    customer = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    has_disliked = serializers.SerializerMethodField()
    cast = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    def get_cast(self, obj):
        casts = CastMember.objects.filter(product=obj.id)
        ser = CastRetriveSerializer(casts, many=True)
        return ser.data

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
    
    def get_owner(self, obj):
        # ser = CustomerDetailSerializer(obj.customer)
        return obj.customer

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
    user = CustomerSerializer()

    class Meta:
        model = Review
        fields = '__all__'


class ReviewAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

class ListAllReviewsGivenSerializer(serializers.ModelSerializer):
    movie = ProductCreateSerializer()

    class Meta:
        model = Review
        fields = '__all__'


class SavedMoviesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedMovies
        fields = '__all__'


class SavedMovieListsSerializer(serializers.ModelSerializer):
    movie = ProductRetriveSerializer()

    class Meta:
        model = SavedMovies
        fields = '__all__'