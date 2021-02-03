import json
import bcrypt
import jwt
import requests
import selenium

from django.views   import View
from django.http    import JsonResponse

from .models        import User
from my_settings    import email_validation, password_validation, SECRET, ALGORITHM

class UserSignUpView(View):
    def post(self, request):
        try:
            data             = json.loads(request.body)
            email            = data["email"]
            password         = data["password"]
            name             = data["name"]
            clean_email      = email_validation(email)
            re_password      = password_validation(password)

            if User.objects.filter(email = email).exists():
                return JsonResponse({"message":"USER_ALREADY_EXIST"}, status = 400)

            clean_password = bcrypt.hashpw(re_password.encode("utf-8"), salt = bcrypt.gensalt()).decode()
            User.objects.create(email = clean_email, password = clean_password, name = name)
            return JsonResponse({"message":"SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        except AttributeError:
            return JsonResponse({"message":"NOT_EMAIL_FORM"}, status = 400)

class UserSignInView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            email       = data["email"]
            password    = data["password"]
            user        = User.objects.get(email = email)

            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                encoded_jwt = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
                return JsonResponse({"message":"SUCCESS", "Authorization":encoded_jwt}, status = 200)
            return JsonResponse({"message":"WRONG_PASSWORD"}, status = 401)
        except User.DoesNotExist:
            return JsonResponse({"message":"USER_DOES_NOT_EXIST"}, status = 401)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 401)
        except ValueError:
            return JsonResponse({"message":"INVALID_SALT"}, status = 403)

class KakaoSignIn(View):
    def post(self, request):
        try:
            data             = json.loads(request.body)
            access_token     = data["access_token"]
            profile_json     = requests.get("https://kapi.kakao.com/v2/user/me", headers = {"Authorization":f"Bearer {access_token}"})
            profile          = profile_json.json()
            nickname         = profile.get("kakao_account")["profile"]["nickname"]
            email            = profile.get("kakao_account")['email']
            user, user_exist = User.objects.get_or_create(email = email, name = nickname)
            encoded_jwt      = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
            return JsonResponse({"Authorization":encoded_jwt}, status = 200)   
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        