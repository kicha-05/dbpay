from rest_framework import serializers
from .models import UserProfile,UserValid,ProductModel,Cart
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [ 'id','name', 'password','email',]


class UserValidSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
    

    def create(self,validated_data):
        return UserValid.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        return instance

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = [ 'id','item','price']

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = [ 'item','price']

        