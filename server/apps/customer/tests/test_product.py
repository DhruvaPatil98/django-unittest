import datetime

from django.test import TestCase
from unittest.mock import patch
from datetime import datetime

from apps.customer.exceptions import (
    ProductDoesNotExistException,
    DiscountCouponDoesNotExistException,
    InsufficientBalanceException,
    TransactionTimeoutException,
    IncorrectDetailsException,
)
from apps.customer.models import Product, DiscountCode
from apps.customer.services.product_service import PurchaseService


class TestPurchaseService(TestCase):

    def setUp(self):
        self.product_id = 'b7ec6681-90c7-4150-9c26-741d7d1a844c'
        self.invalid_product_id = 'c7ec6681-90c7-4150-9c26-741d7d1a844c'
        self.discount_coupon = "DISCOUNT25"
        self.invalid_discount_coupon = "DISCOUNT100"
        self.payment_details = {
            "amount": 50,
            "method": "credit_card"
        }

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

    def test_check_if_product_exists(self):
        result = PurchaseService._check_if_product_exists(self.product_id)
        self.assertIsInstance(result, Product)
        self.assertGreaterEqual(result.in_stock, 1)

    def test_product_does_not_exist(self):
        with self.assertRaises(ProductDoesNotExistException):
            PurchaseService._check_if_product_exists(self.invalid_product_id)

    def test_check_if_discount_coupon_is_valid(self):
        result = PurchaseService._check_if_discount_coupon_is_valid(self.discount_coupon)
        self.assertIsInstance(result, DiscountCode)

    def test_check_if_coupon_does_not_exist(self):
        with self.assertRaises(DiscountCouponDoesNotExistException):
            PurchaseService._check_if_discount_coupon_is_valid(self.invalid_discount_coupon)

    @patch('apps.customer.services.PaymentService.transaction')
    def test_perform_transaction(self, payment_service_mock):
        response_data = {'status': 200}
        payment_service_mock.return_value = response_data
        response = PurchaseService._perform_transaction(self.payment_details)
        self.assertEqual(response['status'], 200)

    @patch('apps.customer.services.PaymentService.transaction')
    def test_post_transaction_operations_success(self, payment_service_mock):
        response_data = {'status': 200}
        payment_service_mock.return_value = response_data
        result = PurchaseService.buy_product(self.product_id, self.discount_coupon, self.payment_details)
        self.assertEqual(result, 'success')

    @patch('apps.customer.services.PaymentService.transaction')
    def test_post_transaction_operations_insufficient_balance(self, payment_service_mock):
        response_data = {'error': 'Insufficient balance'}
        payment_service_mock.return_value = response_data

        with self.assertRaises(InsufficientBalanceException):
            PurchaseService.buy_product(self.product_id, self.discount_coupon, self.payment_details)

    @patch('apps.customer.services.PaymentService.transaction')
    def test_post_transaction_operations_transaction_timeout(self, payment_service_mock):
        response_data = {'error': 'Transaction timeout.'}
        payment_service_mock.return_value = response_data
        with self.assertRaises(TransactionTimeoutException):
            PurchaseService.buy_product(self.product_id, self.discount_coupon, self.payment_details)

    @patch('apps.customer.services.PaymentService.transaction')
    def test_post_transaction_operations_incorrect_details(self, payment_service_mock):
        response_data = {'error': 'Incorrect details'}
        payment_service_mock.return_value = response_data
        with self.assertRaises(IncorrectDetailsException):
            PurchaseService.buy_product(self.product_id, self.discount_coupon, self.payment_details)
