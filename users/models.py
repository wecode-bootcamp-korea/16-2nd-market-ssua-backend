from django.db  import models
from utils      import TimeStampModel

class Grade(models.Model):
    name         = models.CharField(max_length = 45)
    accur_rate   = models.PositiveIntegerField()

    class Meta:
        db_table = "grades"

class User(TimeStampModel):
    email        = models.EmailField(max_length = 245, unique = True)
    password     = models.CharField(max_length = 100)
    name         = models.CharField(max_length = 100)
    address      = models.CharField(max_length = 400)
    grade        = models.ForeignKey("Grade", on_delete = models.CASCADE, default = 6)

    class Meta:
        db_table = "users"

class UserCoupon(models.Model):
    user     = models.ForeignKey("User", on_delete = models.CASCADE)
    coupon   = models.ForeignKey("Coupon", on_delete = models.CASCADE)

    class Meta:
        db_table = "user_coupons"
    
class Coupon(TimeStampModel):
    name             = models.CharField(max_length = 50)
    discount_rate    = models.PositiveIntegerField(null = True)
    discount_price   = models.PositiveIntegerField(null = True)
    end_dt           = models.DateField()
    is_active        = models.BooleanField(default = False)

    class Meta:
        db_table = "coupons"

class Point(TimeStampModel):
    user             = models.ForeignKey("User", on_delete = models.CASCADE)
    point            = models.PositiveIntegerField()
    title            = models.CharField(max_length = 200)
    published_dt     = models.DateField()
    end_dt           = models.DateField()
    status           = models.ForeignKey("PointStatus", on_delete = models.CASCADE)

    class Meta:
        db_table = "points"

class PointStatus(TimeStampModel):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = "point_statuses"

class Destination(models.Model):
    address          = models.CharField(max_length = 200)
    main_address     = models.BooleanField(default = True)
    user             = models.ForeignKey("User", on_delete = models.CASCADE)

    class Meta:
        db_table = "destinations"

class Like(models.Model):
    user     = models.ForeignKey("User", on_delete = models.CASCADE)
    product  = models.ForeignKey("products.ProductGroup", on_delete = models.CASCADE)

    class Meta:
        db_table = "likes"