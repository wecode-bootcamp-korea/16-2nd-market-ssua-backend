from django.urls import path

from .views      import CategoriesView, ProductGroupListView, ProductView

urlpatterns = [
    path('', ProductGroupListView.as_view()),
    path('/categories', CategoriesView.as_view()),
    path('/product-group/<int:product_group_id>', ProductView.as_view()),
]
