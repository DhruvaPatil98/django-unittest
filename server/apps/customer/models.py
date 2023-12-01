from django.db import models

from apps.core.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.PositiveIntegerField(default=0)

    @classmethod
    def get_product_by_id(cls, product_id):
        return cls.objects.filter(id=product_id).first()

    @classmethod
    def reduce_stock_by_1(cls, product_id):
        product = cls.objects.filter(id=product_id).first()
        product.in_stock = product.in_stock - 1
        product.save()


class DiscountCode(BaseModel):
    code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()

    @classmethod
    def get_coupon_by_value(cls, discount_coupon):
        return cls.objects.filter(code=discount_coupon).first()
