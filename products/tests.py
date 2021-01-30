import json

from django.test import Client
from .models     import (
    Product,
    ProductGroup,
    ProductGroupImage,
    ProductGroupPackageType,
    PackageType,
    Category,
    CategoryProduct
)

client = Client()

class CategoryViewTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.category = Category.objects.create(
            name = '반려동물 용품'
        )

    def tearDown(self):
        Category.objects.all().delete()

    def test_category_get_success:
        response = client.get(f'/products/categories/{self.category.id}')
        self.assertEqual(response.status_code, 200)

