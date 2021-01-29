import json

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
    delivery_price   = models.PositiveIntegerField()
    status           = models.ForeignKey("OrderStatus", on_delete = models.CASCADE, default = 1)

    class Meta:
        db_table = "orders"

class OrderStatus(TimeStampModel):
    name    = models.CharField(max_length = 50)
    
    class Meta:
        db_table = "order_status"
    