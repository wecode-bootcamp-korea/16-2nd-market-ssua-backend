import json
import math
import requests
from collections import deque

from django.views               import View
from django.http                import JsonResponse
from django.db.models           import Sum, F, ExpressionWrapper, IntegerField, Q
from django.db.models.functions import Ceil
from django.shortcuts           import redirect

from decorators.utils   import login_required
from .models            import OrderItem, Order
from products.models    import Product
from my_settings        import CLIENT_ID, ADDRESS_URL, COMPANY_LONGITUDE, COMPANY_LATITUDE, DELIVERY_PRICES, ADMIN_KEY, KAKAOPAY_URL

LATITUDE_10KM        = 0.1
LOGITUDU_10KM        = 0.15
DELIVERY_PRICE       = 3000
NONE_DELIVERY_PRICE  = 0
MEET_AMOUNT          = 40000

class OrderView(View):
    @login_required
    def post(self, request):
        try:
            data             = json.loads(request.body)
            user             = request.user
            products_data    = deque(data.values())
            user.order_set.filter()

            if user.order_set.filter(Q(status__name = "결제 대기중") & (Q(delivery_price__in = DELIVERY_PRICES))).exists():
                order = user.order_set.get(status__name = "결제 대기중")
            else:
                order = Order.objects.create(user = user, delivery_price = DELIVERY_PRICE)

            while products_data:
                product_data         = products_data.popleft()
                income_product       = Product.objects.get(id = product_data.get("product_id"))
                existed_products     = order.orderitem_set.all()

                if existed_products.filter(product = income_product).exists():
                    product           = existed_products.get(product = income_product)
                    product.quantity += int(product_data.get("quantity"))
                    product.save()
                else:
                    product = existed_products.create(product = income_product, order = order, quantity = product_data.get("quantity"))
            
            return JsonResponse({"message":'SUCCESS'}, status = 201)
        except Product.DoesNotExist:
            return JsonResponse({"message":"PRODUCT_DOES_NOT_EXIST"}, status = 400)
        except TypeError:
            return JsonResponse({"message":"QUANTITY_REQUIRED"}, status = 400)
        except ValueError:
            return JsonResponse({"message":"PRODUCT_ID_IS_EMPTY"}, status = 400)
        except AttributeError:
            return JsonResponse({"message":"EMPTY_PRODUCT_NUMBER"}, status = 400)

    @login_required
    def get(self, request):
        user                 = request.user 
        params               = {"query": user.address}
        headers              = {"Authorization":f"KakaoAK {CLIENT_ID}"}
        response             = requests.post(ADDRESS_URL, headers = headers, params = params)
        response_json        = response.json()
        documents            = response_json.get("documents")[0]
        latitude             = float(documents.get("x"))
        longitude            = float(documents.get("y"))
        
        if user.order_set.filter(Q(status__name = "결제 대기중") & (Q(delivery_price__in = DELIVERY_PRICES))).exists():
            order = user.order_set.get(status__name = "결제 대기중")
        else:
            order = Order.objects.create(user = user, delivery_price = NONE_DELIVERY_PRICE)

        order.delivery_price = DELIVERY_PRICE

        if latitude < COMPANY_LATITUDE - LATITUDE_10KM or \
        latitude > COMPANY_LATITUDE + LATITUDE_10KM or \
        longitude < COMPANY_LONGITUDE - LOGITUDU_10KM or \
        longitude > COMPANY_LONGITUDE + LOGITUDU_10KM:
            order.delivery_price += DELIVERY_PRICE
        order.save()
    
        context         = {}
        context["id"]   = order.id
        context["user_order_items"] = [
            {
                "order_id"          : user_order.id,
                "product_id"        : user_order.product.id,
                "name"              : user_order.product.name,
                "image_url"         : user_order.product.product_group.thumbnail,
                "price"             : user_order.product.price,
                "discount_rate"     : user_order.product.product_group.discount_rate,
                "discount_price"    : user_order.product.discount_price,
                "quantity"          : user_order.quantity,
                "sold_out"          : "sold out" if user_order.product.sold_out == 1 else "product_exist" ,
                "package_types"     : [product.package_type.name for product in user_order.product.product_group.productgrouppackagetype_set.all()],

            }
            for user_order in order.orderitem_set.all().\
            select_related("product", "product__product_group").\
            prefetch_related("product__product_group__productgrouppackagetype_set")
        ]
        original_price = user.order_set.filter(status__name = "결제 대기중").\
            aggregate(original_sum_price = 
            Sum(F("orderitem__product__price") * F("orderitem__quantity"))).get("original_sum_price")
        
        total_price                  = user.get_total_price
        context["total_price"]       = total_price
        context["point"]             = math.ceil(user.grade.accur_rate * 0.01 * total_price)
        context["delivery_price"]    = order.delivery_price if total_price < MEET_AMOUNT else NONE_DELIVERY_PRICE
        context["user_address"]      = user.address if user.address is not None else "서울특별시 마포구 만리재옛길"

        if original_price is not None:
            context["price_difference"]  = total_price - original_price
        else:
            context["price_difference"]  = 0
            context["delivery_price"]    = 0
        return JsonResponse(context, status = 200)
            
    @login_required
    def patch(self, request):
        try:
            data                 = json.loads(request.body)
            user                 = request.user
            order, order_exist   = user.order_set.get_or_create(status__name = "결제 대기중")
            products_data        = deque(data.values())

            while products_data:
                    product_data         = products_data.popleft()
                    change_product       = Product.objects.get(id = product_data["product_id"])
                    existed_products     = order.orderitem_set.all()
                    product              = existed_products.get(product = change_product)
                    product.quantity     = int(product_data.get("quantity"))
                    product.save()

            return JsonResponse({"message":"CHANGE_QUANTITY"}, status = 200)
        except Product.DoesNotExist:
            return JsonResponse({"message":"PRODUCT_DOES_NOT_EXIST"}, status = 400)
        except OrderItem.DoesNotExist:
            return JsonResponse({"message":"ORDER_ITEM_DOES_NOT_EXIST"}, status = 400)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

    @login_required
    def delete(self, request):
        try:
            data         = json.loads(request.body)
            user         = request.user
            order        = user.order_set.get(status__name = "결제 대기중")
            delete_item  = order.orderitem_set.filter(product_id = int(data["product_id"]))

            if delete_item.exists():
                delete_item.delete()
                return JsonResponse({"message":"DELETE"}, status = 200)
            return JsonResponse({"message":"PRODUCT_DOES_NOT_EXIST"}, status = 400)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

class KakaoPay(View):
    @login_required
    def post(self, request, order_id):
        TAX_FREE             = 0.9
        user                 = request.user
        order                = Order.objects.get(id = order_id)
        total_price          = user.get_total_price
        first_product_name   = order.orderitem_set.first().product.name
        product_count        = len(order.orderitem_set.all())

        params = {
            "cid"                : "TC0ONETIME",
            "partner_order_id"   : "123334556",
            "partner_user_id"    : user.id,
            "item_name"          : f"{first_product_name}외 {product_count}개",
            "quantity"           : "1",
            "total_amount"       : total_price,
            "tax_free_amount"    : int(total_price * TAX_FREE),
            "approval_url"       : "http://127.0.0.1:8000",
            "cancel_url"         : "http://127.0.0.1:8000",
            "fail_url"           : "http://127.0.0.1:8000"
        }

        headers = {
            "Authorization":f"KakaoAK {ADMIN_KEY}",
            "content_type":"application/x-www-form-urlencoded;charset=utf-8"
        }
    
        response         = requests.post(KAKAOPAY_URL, params = params, headers = headers)
        response         = json.loads(response.text)
        redirect_url     = response.get("next_redirect_pc_url")
        return redirect(redirect_url)