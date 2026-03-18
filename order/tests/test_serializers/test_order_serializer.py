from django.test import TestCase

from order.factories import OrderFactory
from product.factories import ProductFactory
from order.serializer.order_serializer import OrderSerializer


class TestOrderSerializer(TestCase):
    """
    Testes unitários para o OrderSerializer.
    Verifica se o serializer serializa/deserializa estrutura corretamente.
    """

    def setUp(self) -> None:
        """
        setUp: executado antes de cada teste para preparar os dados.
        Aqui criamos dois produtos e uma order com ambos produtos.
        """
        self.product_1 = ProductFactory()
        self.product_2 = ProductFactory()

        # Cria uma order com múltiplos produtos usando factory
        self.order = OrderFactory(product=(self.product_1, self.product_2))

        # Serializa a order para testar a saída JSON
        self.order_serializer = OrderSerializer(self.order)

    def test_order_serializer(self):
        """
        Testa se o serializer retorna os dados corretos da order.
        Verifica se:
        1. O primeiro produto tem o título correto
        2. O segundo produto tem o título correto
        """
        # Obtém os dados JSON do serializer
        serializer_data = self.order_serializer.data

        # Verifica se o primeiro produto está com os dados corretos
        self.assertEqual(serializer_data["product"][0]["title"], self.product_1.title)

        # Verifica se o segundo produto está com os dados corretos
        self.assertEqual(serializer_data["product"][1]["title"], self.product_2.title)
