from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.core.serializer import error_response, success_response, response_200
from apps.customer.models import Product

product_param = openapi.Parameter(
    'product_id',
    openapi.IN_QUERY,
    description=f"Product ID",
    type=openapi.TYPE_STRING,
)


class CustomerViewSet(viewsets.ViewSet):
    """
    Customer API
    """

    @swagger_auto_schema(
        tags=["Customer API"],
        responses={400: error_response, 200: success_response},
        operation_summary="List Customer API"
    )
    def get_customers(self, request):
        """
        Api to Request all customers
        """
        response = {'success': 'ok'}
        return response_200(response)

    @swagger_auto_schema(
        tags=["Customer API"],
        manual_parameters=[product_param],
        responses={400: error_response, 200: success_response},
        operation_summary="Get Product API"
    )
    def get_product(self, request):
        """
        Api to Request get product
        """
        product_id = request.GET.get(product_param.name)
        Product.get_product_by_id(product_id)
        response = {'success': 'ok'}
        return response_200(response)

    @swagger_auto_schema(
        tags=["Customer API"],
        responses={400: error_response, 200: success_response},
        operation_summary="Initiate Purchase API"
    )
    def initiate_purchase(self, request):
        """
        Api to initiate the product purchase
        """
        response = {'success': 'ok'}
        return response_200(response)

    @swagger_auto_schema(
        tags=["Customer API"],
        responses={400: error_response, 200: success_response},
        operation_summary="Payment API"
    )
    def make_payment(self, request):
        """
        Api to make payment for the purchase
        """
        response = {'success': 'ok'}
        return response_200(response)


    # purchase
