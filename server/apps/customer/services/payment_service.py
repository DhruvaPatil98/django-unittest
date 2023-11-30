class PaymentService:

    @classmethod
    def transaction(cls, payment_details):
        return {
            'status': 200,
            'error': None,
            'data': payment_details,
        }
