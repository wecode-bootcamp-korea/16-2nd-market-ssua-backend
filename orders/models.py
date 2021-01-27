from django.db  import models
from utils      import TimeStampModel

class OrderItem(TimeStampModel):
    product          = models.ForeignKey("products.Product", on_delete = models.CASCADE)
    order            = models.ForeignKey("Order", on_delete = models.CASCADE)
    quantity         = models.PositiveIntegerField()

    class Meta:
        db_table = "order_items"

class Order(TimeStampModel):
    user             = models.ForeignKey("users.User", on_delete = models.CASCADE)
    user_coupon      = models.ForeignKey("users.UserCoupon", on_delete = models.CASCADE)
    delivery_price   = models.PositiveIntegerField()

    class Meta:
        db_table = "orders"

class OrderStatus(TimeStampModel):
    order   = models.ForeignKey("Order", on_delete = models.CASCADE)
    name    = models.CharField(max_length = 50)
    
    class Meta:
        db_table = "order_status"
    