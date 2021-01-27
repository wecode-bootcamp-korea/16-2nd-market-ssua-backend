from django.db  import models
from utils      import TimeStampModel

class Category(models.Model):
    name = models.CharField(max_length = 120)

    class Meta:
        db_table = "categories"

class CategoryProduct(models.Model):
    category      = models.ForeignKey("Category", on_delete = models.CASCADE)
    product_group = models.ForeignKey("ProductGroup", on_delete = models.CASCADE)

    class Meta:
        db_table = "category_products"

class ProductGroup(TimeStampModel):
    product_group      = models.ManyToManyField("self", through = "Relation")
    name               = models.CharField(max_length = 120)
    sales_unit         = models.CharField(max_length = 120)
    thumbnail          = models.URLField(max_length = 500)
    delivery_type      = models.CharField(max_length = 120, default = "샛별배송/택배배송")
    information        = models.TextField()
    main_description   = models.TextField()
    detail_description = models.TextField()
    discount_rate      = models.PositiveIntegerField()
    price              = models.PositiveIntegerField()

    class Meta:
        db_table = "product_groups"

class Relation(models.Model):
    relate_product_group = models.ForeignKey("ProductGroup", on_delete = models.CASCADE, related_name = "relate")
    related_product_group = models.ForeignKey("ProductGroup", on_delete = models.CASCADE, related_name = "related")

    class Meta:
        db_table = "relations"

class Product(TimeStampModel):
    product_group    = models.ForeignKey("ProductGroup", on_delete = models.CASCADE)
    name             = models.CharField(max_length = 120)
    point            = models.CharField(max_length = 200)
    price            = models.PositiveIntegerField()
    ingredient       = models.CharField(max_length = 120)
    sold_out         = models.BooleanField(default = False)

    class Meta:
        db_table = "products"

class ProductGroupImage(models.Model):
    product_group    = models.ForeignKey("ProductGroup", on_delete = models.CASCADE)
    url              = models.URLField(max_length = 500)
    
    class Meta:
        db_table = "product_group_images"

class ProductGroupPackageType(models.Model):
    product_group    = models.ForeignKey("ProductGroup", on_delete = models.CASCADE)
    package_type     = models.ForeignKey("PackageType", on_delete = models.CASCADE)

    class Meta:
        db_table = "product_group_package_types"

class PackageType(models.Model):
    name = models.CharField(max_length = 120)

    class Meta:
        db_table = "package_types"

class Question(TimeStampModel):
    user             = models.ForeignKey("users.User", on_delete = models.CASCADE)
    product_group    = models.ForeignKey("ProductGroup", on_delete = models.CASCADE)
    title            = models.CharField(max_length = 120)
    content          = models.TextField()
    
    class Meta:
        db_table = "questions"
    