from rest_framework import serializers

from product.models import Product
from product.serializer.category_serializer import CategorySerializer

class ProductSerializer(serializers.Serializer):
    category = serializers.CharField(many=True, required=True)

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'active',
            'category',
            ]