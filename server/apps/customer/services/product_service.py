from apps.customer.exceptions import (
    ProductDoesNotExistException,
    DiscountCouponDoesNotExistException,
    InsufficientBalanceException,
    IncorrectDetailsException,
    TransactionTimeoutException,
)
from apps.customer.models import Product, DiscountCode
from apps.customer.services.payment_service import PaymentService


class PurchaseService:

    @classmethod
    def buy_product(cls, product_id: str, discount_coupon: str, payment_details: dict):
        cls._check_if_product_exists(product_id)
        cls._check_if_discount_coupon_is_valid(discount_coupon)
        response = cls._perform_transaction(payment_details)
        return cls._post_transaction_operations(response, product_id)


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
        error_mapping = {
            "Insufficient balance": InsufficientBalanceException,
            "Incorrect details": IncorrectDetailsException,
            "Transaction timeout": TransactionTimeoutException,
        }
        error = response['error']
        raise error_mapping[error]()

