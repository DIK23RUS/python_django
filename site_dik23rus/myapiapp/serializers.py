from django.contrib.auth.models import Group
from rest_framework import serializers
from shopapp.models import Product, Order


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "pk", "name"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "pk", "name", "price", "archived"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "pk", "delivery_adress", "user", "products"