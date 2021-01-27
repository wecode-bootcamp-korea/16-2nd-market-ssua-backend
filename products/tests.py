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

class ProductViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.product_group = ProductGroup.objects.create(
            name               = '굿키슈',
            sales_unit         = '1팩',
            thumbnail          = 'https://images.unsplash.com/photo-1597843786271-1027c561c6ff?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NTl8fHBldCUyMGZvb2R8ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
            information        = '유통기한 : 제조일로부터 2개월',
            main_description   = '특별한 간식 선물',
            detail_description = '반려동물과의 특별한 날을 더 행복하게 만들어줄 굿키슈를 소개할게요. 순수한 원재료의 맛으로 반려동물의 마음을 두근거리게 하는 간식이에요.',
            price              = 9500,
            discount_rate      = 0
        )

        pk = ProductGroup.objects.get(name='굿키슈').id

        Product.objects.create(
            product_group_id = pk,
            name             = '플레인',
            point            = '키슈 모양으로 만든 반려견용 간식',
            price            = 9500,
            ingredient       = '락토프리우유',
            sold_out         = 0
        )
        ProductGroupImage.objects.create(
            product_group_id = pk,
            url              = 'https://images.unsplash.com/photo-1597843786271-1027c561c6ff?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MzZ8fHBldCUyMGZvb2R8ZW58MHwwfDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60'
        )

        PackageType.objects.create(name = '종이포장')

        package_pk = PackageType.objects.get(name='종이포장').id

        ProductGroupPackageType.objects.create(
            product_group_id = pk,
            package_type_id  = package_pk
        )

    def tearDown(self):
        ProductGroup.objects.all().delete()
        Product.objects.all().delete()
        ProductGroupImage.objects.all().delete()
        PackageType.objects.all().delete()
        ProductGroupPackageType.objects.all().delete()

    def test_product_get_success(self):
        response = client.get(f'/products/product-group/{self.product_group.id}')
        self.assertEqual(response.status_code, 200)

    def test_product_get_does_not_exist(self):
        response = client.get(f'/products/product-group/3456')
        self.assertEqual(response.json(), {"error":"PRODUCT_DOES_NOT_EXIST"})
        self.assertEqual(response.status_code,400)

