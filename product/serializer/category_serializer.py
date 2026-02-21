from rest_framework import serializers

from product.models import category

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = [
            'title',
            'slug',
            'description',
            'active',
            ]