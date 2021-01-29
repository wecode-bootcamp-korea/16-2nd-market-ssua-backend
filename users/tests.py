import json
import bcrypt
import requests
from unittest.mock import patch, MagicMock

from django.test        import TestCase, Client

from .models        import User, Grade
from my_settings    import CLIENT_ID, REDIRECT_URI

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

class UserSignInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Grade.objects.create(id = 6, name = "일반", accur_rate = 1)
        hash_password = bcrypt.hashpw("wecode123".encode("utf-8"), bcrypt.gensalt())
        cls.user     = User.objects.create(
            email    = "ddalkigum@gmail.com", 
            password = hash_password.decode()
            )
    
    def tearDown(self):
        User.objects.all().delete()

    def test_user_sign_in_success(self):
        data = {
            "email":"ddalkigum@gmail.com",
            "password":"wecode123"
        }
        response = client.post("/users/signin", json.dumps(data), content_type = "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "Authorization": response.json().get("Authorization"),
        })
    
    def test_user_sign_in_wrong_password(self):
        data = {
            "email":"ddalkigum@gmail.com",
            "password":"wewewewewewe"
        }
        response = client.post("/users/signin", json.dumps(data), content_type = "application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message":"WRONG_PASSWORD"})

    def test_user_sign_in_user_does_not_exist(self):
        data = {
            "email":"ddalki@gmail.com",
            "password":"wecode123"
        }
        response = client.post("/users/signin", json.dumps(data), content_type = "application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message":"USER_DOES_NOT_EXIST"})

    def test_user_sign_in_key_error(self):
        data = {
            "e":"ddalki@gmail.com",
            "password":"wecode123"
        }
        response = client.post("/users/signin", json.dumps(data), content_type = "application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message":"KEY_ERROR"})        

class UserKakaoSignInTest(TestCase):
    @classmethod
    def setUpTestData(self):
        Grade.objects.create(id = 6, name = "일반", accur_rate = 1)

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_kakao_sign_in_success(self, request):
        class FakeKakaoResponse:
            def json(self):
                return {
                    "kakao_account":{
                        "profile":{
                            "nickname":"딸기검"
                        },
                        "email":"sol3535200@naver.com"
                    }
                }

        access_token = {"access_token": 123456789}
        request.get  = MagicMock(return_value = FakeKakaoResponse())
        response     = client.post('/users/signin/kakao/callback', json.dumps(access_token), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Authorization": response.json().get("Authorization")})

    @patch("users.views.requests")
    def test_kakao_sign_in_key_error(self, request):
        class FakeKakaoResponse:
            def json(self):
                return {
                    "kakao_account":{
                        "profile":{
                            "n":"딸기검"
                        },
                        "email":"sol3535200@naver.com"
                    }
                }

        access_token = {"access_token": 123456789}
        request.get  = MagicMock(return_value = FakeKakaoResponse())
        response     = client.post('/users/signin/kakao/callback', json.dumps(access_token), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"KEY_ERROR"})
