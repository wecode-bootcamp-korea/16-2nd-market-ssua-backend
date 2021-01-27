from django.urls import path

from .views      import CategoriesView, ProductGroupListView, ProductView, QuestionView

urlpatterns = [
    path('', ProductGroupListView.as_view()),
    path('/categories', CategoriesView.as_view()),
    path('/product-group/<int:product_group_id>', ProductView.as_view()),
    path('/product-group/<int:product_group_id>/question', QuestionView.as_view()),
    path('/product-group/<int:product_group_id>/question/<int:question_id>', QuestionView.as_view())
]
