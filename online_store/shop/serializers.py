from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSeriaLizer(serializers.ModelSerializer):
   class Meta:
      model = UserProfile
      fields =('username', 'email', 'password', 'first_name', 'last_name',
                'age', 'phone_number', 'status', 'date_registered')
      extra_kwargs = {'password': {'write_only': True}}

   def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

   def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),

        }




class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = 'all'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = 'all'


class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = ['image']


class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Rating
        fields = ['id', 'user', 'stars']


class ReviewSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer()
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Review
        fields = ['id', 'author', 'text', 'parent_review', 'created_date']


class ProductSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 'price', 'date']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    ratings = RatingSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    product = ProductPhotosSerializer(many=True, read_only=True)
    date = serializers.DateField(format='%d-%m-%Y')
    owner = UserProfileSimpleSerializer()
    average_rating = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 'product', 'description', 'price',
                  'product_video',  'owner', 'active', 'average_rating', 'date', 'ratings', 'reviews']


    def get_average_rating(self,obj):
        return obj.get_average_rating()
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = ['image']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format= '%d-%m-%Y %H:%M')
    date = serializers.DateField(format='%d-%m-%Y')
    class Meta:
        model = Review
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'average_rating', 'date']


    def get_average_rating(self, obj):
        return obj.get_average_rating()


class ProductDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    product = ProductPhotosSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    date = serializers.DateField(format='%d-%m-%Y')
    owner = UserProfileSimpleSerializer()

    class Meta:
        model = Product
        fields = ['product_name', 'category', 'description', 'product', 'price', 'active', 'product_video',
                  'average_rating', 'ratings', 'reviews', 'date', 'owner']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'get_totel_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    totel_price = serializers.SerializerMethodField()

    class Meta:
        model =Cart
        fields = ['id', 'user', 'items', 'totel_price']


    def get_totel_price(self, obj):
        return obj.get_totel_price()
