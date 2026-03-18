from rest_framework import serializers

from product.models import Product
from product.models.category import Category
from product.serializer.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    categories_write = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), write_only=True, source="categories"
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "active",
            "categories",
            "categories_write",
        ]

    def get_categories(self, obj):
        # """Retorna os dados completos das categorias na leitura"""
        return CategorySerializer(obj.categories.all(), many=True).data

    def create(self, validated_data):
        categories_data = validated_data.pop("categories", [])
        product = Product.objects.create(**validated_data)

        for category in categories_data:
            product.categories.add(category)

        return product

    def update(self, instance, validated_data):
        categories_data = validated_data.pop("categories", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categories_data is not None:
            instance.categories.set(categories_data)

        return instance
