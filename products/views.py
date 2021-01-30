import re
import json
import uuid
import boto3

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Count

from .models          import (
    Category,
    CategoryProduct,
    Product,
    ProductGroup,
    ProductGroupImage,
    ProductGroupPackageType,
    Relation
)

class CategoriesView(View):
    def get(self, request):
        categories = Category.objects.all()

        category = [{
            "id" : category.id,
            "name" : category.name
        } for category in categories]

        return JsonResponse({"category": category}, status=200)

class ProductGroupListView(View):
    def get(self, request):
        page = int(request.GET.get('page', 1))

        page_size = 16
        limit     = int(page_size * page)
        offset    = int(limit - page_size)

        category  = request.GET.get('category', None)
        search    = request.GET.get('search', None)
        sort_type = request.GET.get('sort_type', None)

        product_groups = ProductGroup.objects.order_by('id')

        if category:
            product_groups = product_groups.filter(categoryproduct__category_id=category)

        if search:
            product_groups = product_groups.filter(name__icontains=search)

        if sort_type:
            product_groups = product_groups.order_by(sort_type)

        products = [{
            'id'              : product_group.id,
            'name'            : product_group.name,
            'price'           : product_group.price,
            'discount_rate'   : product_group.discount_rate,
            'thumbnail'       : product_group.thumbnail,
            'main_description': product_group.main_description
        } for product_group in product_groups[offset:limit]]

        return JsonResponse({"product_list": products}, status=200)
