import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from product.models import Product
from order.models import Order


class TestOrderViewSet(APITestCase):
    """
    Testes de integração para o OrderViewSet.
    Testa os endpoints HTTP (GET, POST, etc) da estrutura de pedidos.
    """

    client = APIClient()  # Cliente HTTP para fazer requisições simuladas

    def setUp(self):
        """
        setUp: executado antes de cada teste.
        Cria dados iniciais:
        - Uma categoria
        - Um produto nessa categoria
        - Uma order com esse produto
        - um usuário para autenticação
        """
        self.user = UserFactory()

        # Autentica o cliente com um token de usuário
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.category = CategoryFactory(title="technology")

        # Cria um produto com uma categoria associada
        self.product = ProductFactory(
            title="mouse",
            price=100,
            categories=[self.category],  # Associa a categoria ao produto
        )

        # Cria uma order com o produto
        self.order = OrderFactory(product=self.product)

    def test_order(self):
        """
        Testa se o endpoint GET /orders retorna a lista de pedidos corretamente.
        Verifica:
        1. Status code 200 OK
        2. Dados do pedido, produto e categoria estão corretos
        """
        # Faz requisição GET para listar orders
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))

        # Verifica se a requisição foi bem sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extrai o primeiro pedido da resposta JSON
        response_data = json.loads(response.content)
        order_data = response_data["results"][0]

        # Verifica se o produto dentro do pedido tem os dados corretos
        self.assertEqual(order_data["product"][0]["title"], self.product.title)
        self.assertEqual(order_data["product"][0]["price"], self.product.price)
        self.assertEqual(order_data["product"][0]["active"], self.product.active)

        # Verifica se a categoria dentro do produto tem o título correto
        self.assertEqual(
            order_data["product"][0]["categories"][0]["title"],
            self.product.categories.first().title,
        )

    def test_create_order(self):
        """
        Testa se o endpoint POST /orders cria um novo pedido corretamente.
        Verifica:
        1. Status code 201 Created
        2. O pedido foi criado no banco de dados
        3. O usuário do pedido é o esperado
        """
        user = UserFactory()
        product = ProductFactory()

        # Prepara dados para criar um novo pedido
        # Note: product_id em lista porque ordem pode ter múltiplos produtos
        data = json.dumps({"product_id": [product.id], "user": user.id})

        # Faz requisição POST para criar um pedido
        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        # Verifica se o pedido foi criado (status 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifica se a order foi salva no banco de dados com o usuário correto
        created_order = Order.objects.get(user=user)
