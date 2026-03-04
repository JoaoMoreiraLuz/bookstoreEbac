from rest_framework import serializers

from product.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'active',
        ]
        extra_kwargs = {
            'slug': {'required': False}  # Slug não é obrigatório na criação
        }