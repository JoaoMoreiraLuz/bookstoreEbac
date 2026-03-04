import factory

from product.models import Product, Category

# ========== FACTORIES ==========
# Factory Boy é uma biblioteca que cria instâncias de modelos Django para testes
# É muito mais flexível que fixtures e permite customizar dados facilmente

class CategoryFactory(factory.django.DjangoModelFactory):
    """
    Factory para criar instâncias de Category com dados fake.
    
    - factory.Faker('pystr'): gera uma string aleatória
    - factory.Iterator([True, False]): alterna entre True e False a cada criação
    """
    title = factory.Faker('pystr')
    slug = factory.Faker('pystr')
    description = factory.Faker('pystr')
    active = factory.Iterator([True, False])  # Alterna True e False

    class Meta:
        model = Category

class ProductFactory(factory.django.DjangoModelFactory):
    """
    Factory para criar instâncias de Product com dados fake.
    
    Inclui um campo post_generation (categories) que permite
    associar categorias automaticamente ao criar o produto.
    """
    title = factory.Faker('pystr')
    description = factory.Faker('pystr')
    price = factory.Faker('pyint')
    active = factory.Iterator([True, False])

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        """
        Método post_generation: executado APÓS salvar o objeto.
        
        extracted: dados passados como argumento na factory
        Exemplo: ProductFactory(categories=[cat1, cat2])
        
        Precisa checar se extracted é lista ou objeto único,
        porque Factory Boy pode passar ambos.
        """
        if not create:
            # Só executa em estratégia de criação (não em build)
            return

        if extracted:
            # Se extracted não é lista/tuple, converte para lista
            if not isinstance(extracted, (list, tuple)):
                extracted = [extracted]
            # Adiciona cada categoria ao produto
            for category in extracted:
                self.categories.add(category)

    class Meta:
        model = Product