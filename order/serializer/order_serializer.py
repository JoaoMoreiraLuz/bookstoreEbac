from rest_framework import serializers

from django.contrib.auth.models import User
from order.models.order import Order
from product.models import Product
from product.serializer.product_serializer import ProductSerializer


class OrderSerializer(serializers.Serializer):
    """
    Serializer para o modelo Order.

    Note: Usa serializers.Serializer (não ModelSerializer) porque
    precisa customizar bastante o comportamento dos campos relacionados.

    - product: campo read_only que retorna os dados completos dos produtos
    - product_id: campo write_only que aceita IDs dos produtos para criar/atualizar
    - user: campo write_only que aceita o ID do usuário
    - total: campo calculado que soma os preços de todos os produtos
    """

    # Campo read_only: retorna os dados completos dos produtos usando ProductSerializer
    product = ProductSerializer(many=True, read_only=True)

    # Campo write_only: aceita IDs dos produtos para adicionar à order
    # many=True porque uma order pode ter múltiplos produtos
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True, write_only=True
    )

    # Campo write_only: aceita o ID do usuário que fez o pedido
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    # Campo calculado: retorna o total da ordem (soma dos preços dos produtos)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        """
        Método que calcula o total da order somando os preços de todos os produtos.
        obj é a instância da Order sendo serializada.
        """
        total = sum([product.price for product in obj.product.all()])
        return total

    class Meta:
        model = Order
        fields = ["product", "total", "user", "product_id"]
        extra_kwargs = {
            "product": {"required": False}  # Produto não é obrigatório na criação
        }

    def create(self, validated_data):
        """
        Método customizado para criar uma Order.
        Precisa fazer manualmente porque relacionamento many-to-many não é automático no DRF.

        1. Extrai os dados dos produtos e do usuário
        2. Cria a order com o usuário
        3. Adiciona cada produto à order
        """
        # Extrai os dados que precisam de tratamento especial
        product_data = validated_data.pop("product_id")
        user_data = validated_data.pop("user")

        # Cria a order com o usuário
        order = Order.objects.create(user=user_data, **validated_data)

        # Adiciona cada produto à order
        for product in product_data:
            order.product.add(product)

        return order
