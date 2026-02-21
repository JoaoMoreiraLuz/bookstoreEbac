import factory

from product.models import product
from product.models import category

class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('pystr')
    slug = factory.Faker('pystr')
    description = factory.Faker('pystr')
    active = factory.iterators([True, False])

    class Meta:
        model = category

class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.Faker('pyint')
    category = factory.lazyattribute(CategoryFactory)
    title = factory.Faker('pystr')

    @factory.post_generation
    # TALVEZ DÊ ERRO AQUI Ó, ATENÇÃO
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.category.add(category)

    class Meta:
        model = product