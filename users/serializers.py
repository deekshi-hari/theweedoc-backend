from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from django.db.models import OuterRef, Subquery
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from products.models import Product
from products.serializers import ProductCreateSerializer, GenereRetriveSerializer


class MyTokenObtainPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())]) #need to validate email
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password', 'password2')
        #'first_name', 'last_name'

    def validate(self, attrs):
        if attrs['email']=='':
            raise serializers.ValidationError({'error': "email or phonenumber required"})
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"error": "Password fields didn't match."})
        if attrs['phone_number'] != "" and User.objects.filter(phone_number=attrs['phone_number']).exists():
             raise serializers.ValidationError({"error": "Phone number exists"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user


class UsernameValidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'phone_number')


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'designation', 'profile_pic']


class UserSearchSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        if self.context['request'].user.is_authenticated:
            followers_subquery = self.context['followers_subquery_list']
            if obj.id in followers_subquery:
                return True
            return False
        return False

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_pic', 'designation', 'is_following']


class UserProductSerializer(serializers.ModelSerializer):
    genere = GenereRetriveSerializer(many=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    has_disliked = serializers.SerializerMethodField()

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
        fields = ['id', 'title', 'genere', 'age', 'language', 'like_count', 'dislike_count', 'has_liked', 'has_disliked']


class UserDetailSerializer(serializers.ModelSerializer):
    user_filims = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        if self.context['request'].user.is_authenticated:
            print(self.context)
            followers_subquery = self.context['followers_subquery_list']
            if obj.id in followers_subquery:
                return True
            return False
        return False

    def get_user_filims(self, obj):
        request = self.context['request']
        filims = Product.objects.filter(customer=obj.id, status='approved')
        ser = UserProductSerializer(filims, many=True, context={'request':request})
        return ser.data
    
    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'phone_number', 
                  'user_filims', 'followers_count', 'following_count', 'is_following')


class AdminUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'phone_number', 'user_type')