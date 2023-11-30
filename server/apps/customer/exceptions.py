from apps.core.exceptions import BaseException


class ProductDoesNotExistException(BaseException):
    def __init__(self, product):
        self.product = product

    def config(self):
        return {
            'product': self.product
        }

    def __str__(self):
        return f'Product {self.product} is not available'


class ProductOutOfStockException(BaseException):
    def __init__(self, product):
        self.product = product

    def config(self):
        return {
            'product': self.product
        }

    def __str__(self):
        return f'Product {self.product} is out of stock'


class DiscountCouponDoesNotExistException(BaseException):
    def __init__(self, discount_code):
        self.discount_code = discount_code

    def config(self):
        return {
            'discount_code': self.discount_code
        }

    def __str__(self):
        return f'Discount coupon {self.discount_code} is not available'


class InsufficientBalanceException(BaseException):
    def __init__(self):
        self.msg = 'Insufficient Balance'

    def config(self):
        return {
            'error': self.msg
        }

    def __str__(self):
        return self.msg


class IncorrectDetailsException(BaseException):
    def __init__(self):
        self.msg = 'Incorrect Details'

    def config(self):
        return {
            'error': self.msg
        }

    def __str__(self):
        return self.msg


class TransactionTimeoutException(BaseException):
    def __init__(self):
        self.msg = 'Transaction Timeout'

    def config(self):
        return {
            'error': self.msg
        }

    def __str__(self):
        return self.msg
    