import datetime

from django.test import TestCase
from unittest.mock import patch
from datetime import datetime

from apps.customer.exceptions import ProductDoesNotExistException, DiscountCouponDoesNotExistException
from apps.customer.models import Product, DiscountCode
from apps.customer.services.product_service import PurchaseService


class TestPurchaseService(TestCase):

    def setUp(self):
        self.product_id = 'b7ec6681-90c7-4150-9c26-741d7d1a844c'
        self.invalid_product_id = 'c7ec6681-90c7-4150-9c26-741d7d1a844c'
        self.discount_coupon = "DISCOUNT25"
        self.invalid_discount_coupon = "DISCOUNT100"
        # self.discount_id = 'b7ec6681-90c7-4150-9c26-741d7d1a844c'
        self.product = Product(
            id=self.product_id,
            name='Iphone 15',
            description='Iphone 15, 1TB',
            price=150000,
            in_stock=10,
        )
        self.product.save()

        self.discount_code = DiscountCode(
            code=self.discount_coupon,
            discount_amount=100,
            expiration_date=datetime.now()
        )
        self.discount_code.save()

    @patch('apps.customer.models.Product')
    def test_check_if_product_exists(self, product_mock):
        product_mock.get_product_by_id.return_value = Product(id=self.product_id)
        result = PurchaseService._check_if_product_exists(self.product_id)
        self.assertIsInstance(result, Product)

    @patch('apps.customer.models.Product')
    def test_product_does_not_exist(self, product_mock):
        product_mock.get_product_by_id.return_value = None
        with self.assertRaises(ProductDoesNotExistException):
            PurchaseService._check_if_product_exists(self.invalid_product_id)

    @patch('apps.customer.models.DiscountCode')
    def test_check_if_discount_coupon_is_valid(self, discount_code_mock):
        discount_code_mock.get_coupon_by_value.return_value = self.discount_code
        result = PurchaseService._check_if_discount_coupon_is_valid(self.discount_coupon)
        self.assertIsInstance(result, DiscountCode)

    @patch('apps.customer.models.DiscountCode')
    def test_check_if_coupon_does_not_exist(self, product_mock):
        product_mock.get_coupon_by_value.return_value = None
        with self.assertRaises(DiscountCouponDoesNotExistException):
            PurchaseService._check_if_discount_coupon_is_valid(self.invalid_discount_coupon)
