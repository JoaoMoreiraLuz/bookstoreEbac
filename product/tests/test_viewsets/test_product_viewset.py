import json

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from product.factories import CategoryFactory, ProductFactory
from order.factories import OrderFactory, UserFactory
from product.models import Product

class TestProductViewSet(APITestCase):
    """
    Testes de integração para o ProductViewSet.
    Testa os endpoints HTTP (GET, POST, etc) e a lógica de negócio completa.
    """
    
    client = APIClient()  # Cliente HTTP para fazer requisições simuladas

    def setUp(self):
        """
        setUp: executado antes de cada teste.
        Cria dados iniciais para os testes.
        """
        self.user = UserFactory()
        
        # Cria um produto inicial para testes de GET
        self.product = ProductFactory(
            title = 'mouse',
            price = 100.00,
        )

    def test_get_all_products(self):
        """
        Testa se o endpoint GET /products retorna a lista de produtos corretamente.
        Verifica:
        1. Status code 200 OK
        2. Dados do produto na resposta estão corretos
        """
        # Faz requisição GET para listar produtos
        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )

        # Verifica se a requisição foi bem sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extrai o primeiro produto da resposta JSON
        product_data = json.loads(response.content)[0]
        
        # Verifica se os dados retornados correspondem ao produto criado
        self.assertEqual(product_data['title'], self.product.title)
        self.assertEqual(product_data['price'], self.product.price)
        self.assertEqual(product_data['active'], self.product.active)

    def test_create_product(self):
        """
        Testa se o endpoint POST /products cria um novo produto corretamente.
        Verifica:
        1. Status code 201 Created
        2. O produto foi criado no banco de dados
        3. Os dados do produto são os esperados
        """
        category = CategoryFactory()
        
        # Prepara dados para criar um novo produto (note: categories_write para escrita)
        data = json.dumps({
            'title': 'keyboard',
            'price': 150.00,
            'categories_write': [category.id]
        })

        # Faz requisição POST para criar um produto
        response = self.client.post(
            reverse('product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        # Verifica se o produto foi criado (status 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifica se o produto foi salvo no banco de dados com os dados corretos
        created_product = Product.objects.get(title='keyboard')
        self.assertEqual(created_product.price, 150.00)