import json

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from product.factories import CategoryFactory
from product.models import Category


class TestCategoryViewSet(APITestCase):
    """
    Testes de integração para o CategoryViewSet.
    Testa os endpoints HTTP (GET, POST, etc) e a lógica de negócio completa.
    """

    client = APIClient()  # Cliente HTTP para fazer requisições simuladas

    def setUp(self):
        """
        setUp: executado antes de cada teste.
        Cria dados iniciais para os testes.
        """
        # Cria um produto inicial para testes de GET
        self.category = CategoryFactory(title="mouse")

    def test_get_all_categories(self):
        """
        Testa se o endpoint GET /categories retorna a lista de categorias corretamente.
        Verifica:
        1. Status code 200 OK
        2. Dados da categoria na resposta estão corretos
        """
        # Faz requisição GET para listar categorias
        response = self.client.get(reverse("category-list", kwargs={"version": "v1"}))

        # Verifica se a requisição foi bem sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extrai o primeiro produto da resposta JSON
        response_data = json.loads(response.content)
        category_data = response_data["results"][0]

        # Verifica se os dados retornados correspondem à categoria criada
        self.assertEqual(category_data["title"], self.category.title)

    def test_create_category(self):
        """
        Testa se o endpoint POST /categories cria uma nova categoria corretamente.
        Verifica:
        1. Status code 201 Created
        2. A categoria foi criada no banco de dados
        3. Os dados da categoria são os esperados
        """
        # Prepara dados para criar uma nova categoria (note: categories_write para escrita)
        data = json.dumps({"title": "eletronicos"})

        # Faz requisição POST para criar uma categoria
        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        # Verifica se o produto foi criado (status 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifica se o produto foi salvo no banco de dados com os dados corretos
        created_category = Category.objects.get(title="eletronicos")
        self.assertEqual(created_category.title, "eletronicos")
