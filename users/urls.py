from django.urls import path

from .views import UserSignUpView, UserSignInView, KakaoSignIn

urlpatterns = [
    path("/signup", UserSignUpView.as_view()),
    path("/signin", UserSignInView.as_view()),
    path("/signin/kakao/callback", KakaoSignIn.as_view())
]