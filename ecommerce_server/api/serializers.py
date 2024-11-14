# serializers.py

from rest_framework import serializers
from .models import Product
from rest_framework_mongoengine import serializers

class ProductSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Product
        fields = '__all__'


from .models import Category

class CategorySerializer(serializers.DocumentSerializer):
    class Meta:
        model = Category
        fields = '__all__'