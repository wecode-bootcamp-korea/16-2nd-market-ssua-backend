from django.urls import path

from .views import OrderView, KakaoPay

urlpatterns = [
    path("", OrderView.as_view()),
    path("/<int:order_id>/payment/kakao", KakaoPay.as_view())
]
