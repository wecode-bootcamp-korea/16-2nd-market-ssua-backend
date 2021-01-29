import jwt

from django.http    import JsonResponse

from users.models import User
from my_settings  import SECRET, ALGORITHM

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token           = request.headers.get("Authorization")
            user_id         = jwt.decode(token, key = SECRET, algorithms = ALGORITHM).get("id")
            user            = User.objects.get(id = user_id)
            request.user    = user

        except User.DoesNotExist:
            return JsonResponse({"message":"USER_DOES_NOT_EXIST"}, status = 400)
        except jwt.InvalidSignatureError:
            return JsonResponse({"message":"INVALID_SIGNATURE"}, status = 400)
        except jwt.DecodeError:
            return JsonResponse({"message":"DECODE_ERROR"}, status = 400)
        return func(self, request, *args, **kwargs)
    return wrapper