from rest_framework import serializers

from product.models import Product
from product.serializer.product_serializer import ProductSerializer

class OrderSerializer(serializers.Serializer):
    product = ProductSerializer(required=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        total = sum([product.price for product in istance.product.all()])
        return total
    
    class meta:
        model = Product
        fields = ['product', 'total']