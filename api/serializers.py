from rest_framework import serializers
from api.models import Products, Carts,Reviews
from django.contrib.auth.models import User

#used for changing the query set to python native form

class ProductsSerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    name=serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    category = serializers.CharField()
    image = serializers.ImageField()

class ProductModelSerializer(serializers.ModelSerializer):
    avg_rating=serializers.CharField(read_only=True)
    no_rating=serializers.CharField(read_only=True)
    class Meta:
        model=Products
        fields='__all__' #if not all fields are required, enter the required fields as a list ['name','etc']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CartSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    class Meta:
        model= Carts
        fields='__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    product=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)

    class Meta:
        model= Reviews
        fields='__all__'

