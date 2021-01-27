import json
import jwt

from django.test  import TestCase, Client

from my_settings   import SECRET, ALGORITHM
from users.models  import User, Grade
from .models       import (
    Product,
    ProductGroup,
    ProductGroupImage,
    ProductGroupPackageType,
    PackageType,
    Category,
    CategoryProduct,
    Question
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

    def test_category_get_success(self):
        response = client.get(f'/products/categories/{self.category.id}')
        self.assertEqual(response.status_code, 200)

class ProductViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.product_group = ProductGroup.objects.create(
            name               = '굿키슈',
            sales_unit         = '1팩',
            thumbnail          = 'https://images.unsplash.com/photo-1597843786271-1027c561c6ff?',
            information        = '유통기한 : 제조일로부터 2개월',
            main_description   = '특별한 간식 선물',
            detail_description = '반려동물과의 특별한 날을 더 행복하게 만들어줄 굿키슈를 소개할게요.',
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
            url              = 'https://images.unsplash.com/photo-1597843786271-1027c561c6ff?'
        )

        PackageType.objects.create(name = '종이포장')

        package_pk = PackageType.objects.get(name='종이포장').id

        ProductGroupPackageType.objects.create(
            product_group_id = pk,
            package_type_id  = package_pk
        )

        Grade.objects.create(name = "일반", accur_rate = 1, id = 6)

        user = User.objects.create(
            email    = 'sua@wecode.com',
            password = 'code1234',
            name     = '수아',
            address  = '테헤란로 427'
        )

        test_user = User.objects.get(name='수아')

        question = Question.objects.create(
            user_id          = test_user.id,
            product_group_id = pk,
            title            = 'test',
            content          = '유닛테스트~'
        )

    def tearDown(self):
        ProductGroup.objects.all().delete()
        Product.objects.all().delete()
        ProductGroupImage.objects.all().delete()
        PackageType.objects.all().delete()
        ProductGroupPackageType.objects.all().delete()
        User.objects.all().delete()
        Question.objects.all().delete()
        Grade.objects.all.delete()

    def test_product_get_success(self):
        response = client.get(f'/products/product-group/{self.product_group.id}')
        self.assertEqual(response.status_code, 200)

    def test_product_get_does_not_exist(self):
        response = client.get(f'/products/product-group/3456')
        self.assertEqual(response.json(), {"error":"PRODUCT_DOES_NOT_EXIST"})
        self.assertEqual(response.status_code,400)

class QuestionViewTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        Grade.objects.create(name = "일반", accur_rate = 1, id = 6)
        user = User.objects.create(
            email    = 'sua@wecode.com',
            password = 'code1234',
            name     = '수아',
            address  = '테헤란로 427'
        )

        self.test_user = User.objects.get(name='수아')

        self.product_group = ProductGroup.objects.create(
            name               = '굿키슈',
            sales_unit         = '1팩',
            thumbnail          = 'https://images.unsplash.com/photo-1597843786271-1027c561c6ff?',
            information        = '유통기한 : 제조일로부터 2개월',
            main_description   = '특별한 간식 선물',
            detail_description = '반려동물과의 특별한 날을 더 행복하게 만들어줄 굿키슈를 소개할게요.',
            price              = 9500,
            discount_rate      = 0
         )

        product_group_id = ProductGroup.objects.get(name='굿키슈').id

        self.question = Question.objects.create(
            user_id          = self.test_user.id,
            product_group_id = product_group_id,
            title            = 'test',
            content          = '유닛테스트~'
        )

    def tearDown(self):
        Question.objects.all().delete()
        User.objects.all().delete()
        ProductGroup.objects.all().delete()
        Grade.objects.all().delete()

    def test_question_post_success(self):
        user          = self.test_user
        product_group = self.product_group

        token  = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        header = {"HTTP_Authorization" : token}

        data = {
            "user_id"          : user.id,
            "product_group_id" : product_group.id,
            "title"            : "test",
            "content"          : "test"
        }
        response = client.post(f"/products/product-group/{self.product_group.id}/question", json.dumps(data), **header, content_type = "application/json")
        self.assertEqual(response.status_code, 201)

    def test_question_post_Key_error(self):
        user          = self.test_user
        product_group = self.product_group

        token  = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        header = {"HTTP_Authorization" : token}

        data = {
            "user_id"          : user.id,
            "product_group_id" : product_group.id,
            "content"          : "key error"
            }

        response = client.post(f'/products/product-group/{self.product_group.id}/question', json.dumps(data), **header, content_type = "application/json")
        self.assertEqual(response.status_code, 400)

    def test_question_put_success(self):
        user          = self.test_user
        product_group = self.product_group

        token  = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        header = {"HTTP_Authorization" : token}

        data = {
            "user_id"          : user.id,
            "product_group_id" : product_group.id,
            "title"            : "change",
            "content"          : "change test"
        }
        response = client.put(f'/products/product-group/{self.product_group.id}/question/{self.question.id}', json.dumps(data), **header, content_type = "application/json")
        self.assertEqual(response.status_code, 200)

    def test_question_put_does_not_exist(self):
        user          = self.test_user
        product_group = self.product_group

        token  = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        header = {"HTTP_Authorization" : token}

        data = {
            "user_id"          : user.id,
            "product_group_id" : product_group.id,
            "title"            : "error",
            "content"          : "error"
        }
        response = client.put(f'/products/product-group/{self.product_group.id}/question/3364', json.dumps(data), **header, content_type = "application/json")
        self.assertEqual(response.status_code, 400)

    def test_question_delete_success(self):
        user          = self.test_user
        product_group = self.product_group

        token  = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        header = {"HTTP_Authorization" : token}

        data = {
            "user_id" : user.id,
            "product_group_id" : product_group.id
        }

        response = client.delete(f'/products/product-group/{self.product_group.id}/question/{self.question.id}', json.dumps(data), **header, content_type = "application/json")
        self.assertEqual(response.status_code, 200)

    def test_question_delete_does_not_exist(self):
        user          = self.test_user
        product_group = self.product_group

        token  = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        header = {"HTTP_Authorization" : token}

        data = {
            "user_id" : user.id,
            "product_group_id" : product_group.id
        }

        response = client.delete(f'/products/product-group/{self.product_group.id}/question/3388', json.dumps(data), **header, content_type = "application/json")
        self.assertEqual(response.status_code, 400)
