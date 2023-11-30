from django.contrib import admin
from apps.core.admin import BaseAdmin
from apps.customer.models import Product, DiscountCode


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ('id', 'name', 'description', 'price', 'in_stock')
    search_fields = ['name']


@admin.register(DiscountCode)
class DiscountCodeAdmin(BaseAdmin):
    list_display = ('id', 'code', 'is_active', 'discount_amount', 'expiration_date')
    search_fields = ['code']
    # list_filter = ['code']
