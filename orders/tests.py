import json
import jwt

from django.test    import TestCase, Client

from users.models        import User, Grade
from orders.models       import Order, OrderItem, OrderStatus
from products.models     import (Product, 
                                ProductGroup, 
                                Category, 
                                PackageType, 
                                ProductGroupPackageType)

from my_settings         import SECRET, ALGORITHM

client = Client()

class OrderTest(TestCase):
    maxDiff = None
    @classmethod
    def setUpTestData(cls):
        OrderStatus.objects.create(name = "결제 대기중")
        Grade.objects.create(name = "일반", accur_rate = 1, id = 6)
        cls.user     = User.objects.create(
            email    = "ddalkigum@gmail.com", 
            name     = "딸기검", 
            password = "wecode123", 
            address  = "테헤란로 81길"
            )

        category     = Category.objects.create(name = "강아지 간식")
        package_type = PackageType.objects.create(name = "냉동/종이포장")
        cls.order    = Order.objects.create(
            user = cls.user,
            delivery_price = 3000
        )

        product_group = ProductGroup.objects.create(
            name                 = "강아지 수제 간식",
            sales_unit           = "1팩",
            thumbnail            = "https://images.unsplash.com/photo-1582798358481-d199fb7347bb?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NXx8cGV0JTIwZm9vZHxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
            delivery_type        = "샛별배송",
            information          = "강아지용입니다",
            main_description     = "강아지입니다",
            detail_description   = "강아지가 먹는 간식입니다", 
            discount_rate        = 20,
            price                = 10000
        )
        
        ProductGroupPackageType.objects.create(product_group = product_group, package_type = package_type)

        product = Product.objects.create(
            product_group    = product_group,
            name             = "연어롤",
            point            = "강아지 전용",
            price            = 15000,
            ingredient       = "노르웨이산 연어",
            sold_out         = 0
        )
        
        product_2 = Product.objects.create(
            product_group    = product_group,
            name             = "연어 초밥",
            point            = "고양이 전용",
            price            = 50000,
            ingredient       = "노르웨이산 연어",
            sold_out         = 0
        )
        cls.product_2 = product_2
        cls.order_item = OrderItem.objects.create(product = product, order = cls.order, quantity = 2)
        cls.product_group = product_group

    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()
        PackageType.objects.all().delete()
        ProductGroup.objects.all().delete()
        User.objects.all().delete()
        Grade.objects.all().delete()
        OrderStatus.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()

    def test_order_add_product(self):
        order    = self.order
        user     = self.user
        data     = {
            "product_1": {
                "product_id"    : "1",
                "quantity"      : "1"
        }
        }   
        token    = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        response = client.post("/orders", json.dumps(data),  **{"HTTP_Authorization" : token}, content_type = "application/json")
        self.assertEqual(response.status_code, 201)

    def test_order_key_error(self):
        order    = self.order
        user     = self.user
        data     = {
            "product_1": {
                "p": "1",
                "q": "1"
            }
        }
        token    = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        response = client.post("/orders", json.dumps(data), **{"HTTP_Authorization": token}, content_type = "application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_user_order_products(self):
        order    = self.order
        user     = self.user

        token    = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        response = client.get("/orders", **{"HTTP_Authorization":token}, content_type = "application/json")
        self.assertEqual(response.json(), 
        {
            "id"                : 1,
            "user_order_items"  :[
            {
                "order_id"          : 1,
                "product_id"        : 1,
                "name"              : "연어롤",
                "image_url"         : "https://images.unsplash.com/photo-1582798358481-d199fb7347bb?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NXx8cGV0JTIwZm9vZHxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
                "price"             : 15000,
                "discount_rate"     : 20,
                "discount_price"    : 12000,
                "quantity"          : 2,
                "sold_out"          : "product_exist",
                "package_types"     : ["냉동/종이포장"]
            }
        ],  "delivery_price"    : 3000,
            "point"             : 240,
            "user_address"      : "테헤란로 81길",
            "price_difference"  : -6000
        }
        )

    def test_get_user_order_products_delivery_price_surcharge(self):
        order        = self.order
        user         = self.user
        user.address = "부산광역시"
        user.save()

        token    = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        response = client.get("/orders", **{"HTTP_Authorization":token}, content_type = "application/json")
        self.assertEqual(response.json(), 
        {
            "id"                : 1,
            "user_order_items":[
            {
                "order_id"          : 1,
                "product_id"        : 1,
                "name"              : "연어롤",
                "image_url"         : "https://images.unsplash.com/photo-1582798358481-d199fb7347bb?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NXx8cGV0JTIwZm9vZHxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
                "price"             : 15000,
                "discount_rate"     : 20,
                "discount_price"    : 12000,
                "quantity"          : 2,
                "sold_out"          : "product_exist",
                "package_types"     : ["냉동/종이포장"]
            }
        ],  "delivery_price"    : 6000,
            "point"             : 240,
            "user_address"      : "부산광역시",
            "price_difference"  : -6000
        }
        )

    def test_get_user_order_products_none_delivery_price(self):
        order        = self.order
        user         = self.user
        
        order_item = OrderItem.objects.create(order = order, product = self.product_2, quantity = 1)

        token    = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        response = client.get("/orders", **{"HTTP_Authorization":token}, content_type = "application/json")
        self.assertEqual(response.json(), 
        {
            "id"                : 1,
            "user_order_items":[
            {
                "order_id"          : 1,
                "product_id"        : 1,
                "name"              : "연어롤",
                "image_url"         : "https://images.unsplash.com/photo-1582798358481-d199fb7347bb?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NXx8cGV0JTIwZm9vZHxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
                "price"             : 15000,
                "discount_rate"     : 20,
                "discount_price"    : 12000,
                "quantity"          : 2,
                "sold_out"          : "product_exist",
                "package_types"     : ["냉동/종이포장"]
            },
            {
                "order_id"          : 2,
                "product_id"        : 2,
                "name"              : "연어 초밥",
                "image_url"         : "https://images.unsplash.com/photo-1582798358481-d199fb7347bb?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NXx8cGV0JTIwZm9vZHxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
                "price"             : 50000,
                "discount_rate"     : 20,
                "discount_price"    : 40000,
                "quantity"          : 1,
                "sold_out"          : "product_exist",
                "package_types"     : ["냉동/종이포장"]
            },
        ],  "delivery_price"    : 0,
            "point"             : 640,
            "user_address"      : "테헤란로 81길",
            "price_difference"  : -16000
        }
        )

    def test_change_product_quantity(self):
        order    = self.order
        user     = self.user
        data     = {
            "product_1": {
                "product_id"    : "1",
                "quantity"      : "3"
        }
        }  

        token    = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        response = client.patch("/orders", data = json.dumps(data), **{"HTTP_Authorization":token}, content_type = "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message":"CHANGE_QUANTITY"})

    def test_change_product_quantity_key_error(self):
        order    = self.order
        user     = self.user
        data     = {
            "product_1": {
                "produ_id"    : "1",
                "quantity"    : "3"
        }
        }  

        token    = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        response = client.patch("/orders", data = json.dumps(data), **{"HTTP_Authorization":token}, content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"KEY_ERROR"})

    def test_change_product_quantity_product_does_not_exist(self):
        order    = self.order
        user     = self.user
        data     = {
            "product_1": {
                "product_id"  : "50",
                "quantity"    : "3"
        }
        }  

        token    = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        response = client.patch("/orders", data = json.dumps(data), **{"HTTP_Authorization":token}, content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"PRODUCT_DOES_NOT_EXIST"})

    def test_change_product_quantity_order_item_does_not_exist(self):
        order    = self.order
        user     = self.user
        data     = {
            "product_1": {
                "product_id"  : "2",
                "quantity"    : "3"
        }
        }  

        token    = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        response = client.patch("/orders", data = json.dumps(data), **{"HTTP_Authorization":token}, content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"ORDER_ITEM_DOES_NOT_EXIST"})

    def test_delete_product(self):
        order = self.order
        user = self.user

        data = {
            "product_id":"1"
        }

        token    = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        response = client.delete("/orders", data = json.dumps(data), **{"HTTP_Authorization":token}, content_type = "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message":"DELETE"})

    def test_delete_product_does_not_exist(self):
        order = self.order
        user = self.user

        data = {
            "product_id":"20"
        }

        token    = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        response = client.delete("/orders", data = json.dumps(data), **{"HTTP_Authorization":token}, content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"PRODUCT_DOES_NOT_EXIST"})