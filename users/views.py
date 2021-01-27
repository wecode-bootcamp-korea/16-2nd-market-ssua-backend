import json
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse

from .models import User
from my_settings import email_validation, password_validation

class UserSignUpView(View):
    def post(self, request):
        try:
            data             = json.loads(request.body)
            email            = data["email"]
            password         = data["password"]
            name             = data["name"]
            address          = data.get("address")
            clean_email      = email_validation(email)
            re_password      = password_validation(password)

            if User.objects.filter(email = email).exists():
                return JsonResponse({"message":"USER_ALREADY_EXIST"}, status = 400)

            clean_password = bcrypt.hashpw(re_password.encode("utf-8"), salt = bcrypt.gensalt()).decode()
            User.objects.create(email = email, password = clean_password, name = name, address = address)
            return JsonResponse({"message":"SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        except AttributeError:
            return JsonResponse({"message":"NOT_EMAIL_FORM"}, status = 400)
