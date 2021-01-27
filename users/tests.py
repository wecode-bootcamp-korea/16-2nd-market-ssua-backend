import json

from django.test    import TestCase, Client

from .models        import User, Grade

client = Client()

class UserSignUpTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Grade.objects.create(name = "일반", accur_rate = 1, id = 6)
        cls.user     = User.objects.create(
            email    = "ddalkigum@gmail.com", 
            name     = "딸기검", 
            password = "wecode123", 
            address  = "테헤란로 81길"
            )
        
    def tearDown(self):
        User.objects.all().delete()
    def test_user_sign_up_success(self):
        data = {
            "email" : "ddalkigum@gmail.com",
            "name" : "딸기검",
            "password" : "wecode123",
            "address" : "테헤란로 81길"
        }
        response = client.post("/users/signup", json.dumps(data), content_type = "application/json")
        self.assertEqual(self.user.name, data.get("name"))

    def test_user_sign_up_key_error(self):
        data = {
            "e"        : "ddalki@gmail.com",
            "name"     : "딸기검",
            "password" : "wecode123",
            "address"  : "테헤란로 81길"
        }
        response = client.post("/users/signup", json.dumps(data), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

    def test_user_sign_up_attribute_error(self):
        data = {
            "email"    : "ddalki",
            "name"     : "딸기검",
            "password" : "wecode123",
            "address"  : "테헤란로 81길"
        }
        response = client.post("/users/signup", json.dumps(data), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "NOT_EMAIL_FORM"})

    def test_user_sign_up_user_exist(self):
        data = {
            "email"    : "ddalkigum@gmail.com",
            "name"     : "딸기검",
            "password" : "wecode123",
            "address"  : "테헤란로 81길"
        }
        response = client.post("/users/signup", json.dumps(data), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "USER_ALREADY_EXIST"})
