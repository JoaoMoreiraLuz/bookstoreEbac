import factory

from django.contrib.auth.models import User
from product.factories import ProductFactory

from order.models import Order

# ========== FACTORIES ==========
# Factories para criar dados de teste realistas

class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory para criar instâncias de User (Django built-in model).
    
    Cada factory pode gerar dados diferentes automaticamente.
    """
    email = factory.Faker('pystr')      # Email aleatório (string)
    username = factory.Faker('pystr')   # Username aleatório

    class Meta:
        model = User

class OrderFactory(factory.django.DjangoModelFactory):
    """
    Factory para criar instâncias de Order com um usuário automaticamente.
    
    - SubFactory(UserFactory): cria um usuário automaticamente para cada order
    - post_generation(product): permite associar produtos após criar a order
    """
    
    # SubFactory: cria um user automaticamente quando cria uma order
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        """
        Método post_generation para associar produtos à order.
        
        extracted: produtos passados como argumento
        Exemplo: OrderFactory(product=produto1)  ou  OrderFactory(product=[prod1, prod2])
        
        Precisa checar tipo porque pode receber um objeto único ou uma lista.
        """
        if not create:
            # Só executa em estratégia de criação (não em build)
            return

        if extracted:
            # Se extracted não é lista/tuple, converte para lista
            # Assim funciona com ambos: OrderFactory(product=p) e OrderFactory(product=[p1, p2])
            if not isinstance(extracted, (list, tuple)):
                extracted = [extracted]
            # Adiciona cada produto à order
            for product in extracted:
                self.product.add(product)

    class Meta:
        model = Order
