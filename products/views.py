import re
import json

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Count
from decorators.utils   import login_required

from users.models     import User
from .models          import (
    Category,
    CategoryProduct,
    Product,
    ProductGroup,
    ProductGroupImage,
    ProductGroupPackageType,
    Relation,
    Question
)

class CategoriesView(View):
    def get(self, request):
        categories = Category.objects.all()

        category = [{
            "id"   : category.id,
            "name" : category.name
        } for category in categories]

        return JsonResponse({"category": category}, status=200)

class ProductGroupListView(View):
    def get(self, request):
        page = int(request.GET.get('page', 1))

        context   = {}
        page_size = 16
        limit     = int(page_size * page)
        offset    = int(limit - page_size)

        category  = request.GET.get('category', None)
        search    = request.GET.get('search', None)
        sort_type = request.GET.get('sort_type', None)

        product_groups = ProductGroup.objects.order_by('?')

        if category:
            product_groups = product_groups.filter(categoryproduct__category_id=category)

        if search:
            product_groups = product_groups.filter(name__icontains=search)

        if sort_type:
            product_groups = product_groups.order_by(sort_type)
        
        context[f"product_group_{category}_{search}_{sort_type}_{page}"] = [{
            'id'              : product_group.id,
            'name'            : product_group.name,
            'price'           : product_group.price,
            'discount_rate'   : product_group.discount_rate,
            'thumbnail'       : product_group.thumbnail,
            'main_description': product_group.main_description
        } for product_group in product_groups[offset:limit]]
        return JsonResponse(context, status=200)

class ProductView(View):
    def get(self, request, product_group_id):
        try:
            product_group    = ProductGroup.objects.get(id = product_group_id)
            product_packages = product_group.productgrouppackagetype_set.all()
            context          = {}
            context["result"] = {
                "product_group_id"   : product_group.id,
                "product_group_name" : product_group.name,
                "sales_unit"         : product_group.sales_unit,
                "thumbnail"          : product_group.thumbnail,
                "delivery_type"      : product_group.delivery_type,
                "information"        : product_group.information,
                "main_description"   : product_group.main_description,
                "detail_description" : product_group.detail_description,
                "discount_rate"      : product_group.discount_rate,

                "package_type" : product_packages[0].package_type.name,

                "product_group_images" : [{
                    "url" : image.url
                } for image in product_group.productgroupimage_set.all()],

                "products" : [{
                    "id"         : product.id,
                    "name"       : product.name,
                    "price"      : product.price,
                    "sold_out"   : product.sold_out,
                    "ingredient" : product.ingredient,
                    "point"      : product.point
                } for product in product_group.product_set.all()],

                "related_product" : [{
                    "related_product_id"        : relate_product.related_product_group.id,
                    "related_product_name"      : relate_product.related_product_group.name,
                    "related_product_price"     : relate_product.related_product_group.price,
                    "related_product_thumbnail" : relate_product.related_product_group.thumbnail
                } for relate_product in product_group.relate.select_related("related_product_group")],

                "question" :[{
                    "product_group_id" : question.product_group.id,
                    "question_id"      : question.id,
                    "user_name"        : question.user.name,
                    "title"            : question.title,
                } for question in product_group.question_set.all()]
            }
            return JsonResponse(context, status=200)

        except ProductGroup.DoesNotExist:
            return JsonResponse({"error": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class QuestionView(View):
    @login_required
    def post(self, request, product_group_id):
        try:
            data = json.loads(request.body)

            Question.objects.create(
                user             = request.user,
                product_group_id = product_group_id,
                title            = data['title'],
                content          = data['content']
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"error": "KEY_ERROR"}, status=400)

    @login_required
    def put(self, request, product_group_id, question_id):
        try:
            data     = json.loads(request.body)
            question = Question.objects.get(user = request.user, id = question_id)

            question.title   = data.get('title')
            question.content = data.get('content')
            question.save()

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except Question.DoesNotExist:
            return JsonResponse({"error": "QUESTION_DOES_NOT_EXIST"}, status=400)

    @login_required
    def delete(self, request, product_group_id, question_id):
        try:
            Question.objects.get(user = request.user, id = question_id).delete()
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except Question.DoesNotExist:
            return JsonResponse({"error": "QUESTION_DOES_NOT_EXIST"}, status=400)
