from django.urls import path

from .views      import CategoriesView, ProductGroupListView

urlpatterns = [
    path('', ProductGroupListView.as_view()),
    path('/categories', CategoriesView.as_view()),
]
