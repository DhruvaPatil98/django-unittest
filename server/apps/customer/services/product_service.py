from apps.customer.exceptions import (
    ProductDoesNotExistException,
    DiscountCouponDoesNotExistException,
    InsufficientBalanceException,
    IncorrectDetailsException,
    ProductOutOfStockException,
    TransactionTimeoutException,
)
from apps.customer.models import Product, DiscountCode
from apps.customer.services.payment_service import PaymentService


# Version 1: Basic Function for transaction
class PurchaseServiceV1:

    @classmethod
    def buy_product(cls, product_id: str, discount_coupon: str, payment_details: dict):
        product_obj = Product.objects.filter(id=product_id)
        if not product_obj:
            raise ProductDoesNotExistException(product_id)
        if product_obj.in_stock == 0:
            raise ProductOutOfStockException(product_id)

        discount_coupon_obj = DiscountCode.objects.filter(discount_coupon=discount_coupon)
        if not discount_coupon_obj:
            raise DiscountCouponDoesNotExistException(discount_coupon)

        response = PaymentService.transaction(payment_details)
        if response['status'] == 200:
            product_obj.stock = product_obj.stock - 1
            product_obj.save()
            return "success"
        if response['error'] == "Insufficient balance":
            raise InsufficientBalanceException()
        if response['error'] == "Incorrect details":
            raise IncorrectDetailsException()
        if response['error'] == "Transaction timeout.":
            raise TransactionTimeoutException()


"""
- Initially, expired discount codes are removed from the system, so code works fine.
- Now we update code to only mark the expired discount code as is_active = False, now this code breaks.

Unit tests for this:
1. Discount code is being used, and it is correct - Positive test case
2. Discount code is being used, and it has expired - Negative test case

"""


# Version 2: Separation of Logic and ORM queries
class PurchaseServiceV2:

    @classmethod
    def buy_product(cls, product_id: str, discount_coupon: str, payment_details: dict):
        product_obj = Product.get_product_by_id(product_id)
        if not product_obj:
            raise ProductDoesNotExistException(product_id)

        discount_coupon_obj = DiscountCode.get_coupon_by_value(discount_coupon=discount_coupon)
        if not discount_coupon_obj:
            raise DiscountCouponDoesNotExistException(discount_coupon)

        response = PaymentService.transaction(payment_details)
        if response['status'] == 200:
            Product.reduce_stock_by_1(product_id)
            return "success"
        if response['error'] == "Insufficient balance":
            raise InsufficientBalanceException()
        if response['error'] == "Incorrect details":
            raise IncorrectDetailsException()
        if response['error'] == "Transaction timeout.":
            raise TransactionTimeoutException()


# Version 3: Unit functions

class PurchaseService:
    @classmethod
    def _check_if_product_exists(cls, product_id):
        product_obj = Product.get_product_by_id(product_id)
        if not product_obj:
            raise ProductDoesNotExistException(product_id)
        return product_obj

    @classmethod
    def _check_if_discount_coupon_is_valid(cls, discount_coupon):
        discount_coupon_obj = DiscountCode.get_coupon_by_value(discount_coupon=discount_coupon)
        if not discount_coupon_obj:
            raise DiscountCouponDoesNotExistException(discount_coupon)
        return discount_coupon_obj

    @classmethod
    def _perform_transaction(cls, payment_details):
        return PaymentService.transaction(payment_details)

    @classmethod
    def _post_transaction_operations(cls, response, product_id):
        if response.get('status') == 200:
            Product.reduce_stock_by_1(product_id)
            return "success"
        if response.get('error') == "Insufficient balance":
            raise InsufficientBalanceException()
        if response.get('error') == "Incorrect details":
            raise IncorrectDetailsException()
        if response.get('error') == "Transaction timeout.":
            raise TransactionTimeoutException()

    @classmethod
    def buy_product(cls, product_id: str, discount_coupon: str, payment_details: dict):
        cls._check_if_product_exists(product_id)
        cls._check_if_discount_coupon_is_valid(discount_coupon)
        response = cls._perform_transaction(payment_details)
        return cls._post_transaction_operations(response, product_id)


