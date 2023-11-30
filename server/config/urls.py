from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.core.utils import BothHttpAndHttpsSchemaGenerator
from apps.customer.views import CustomerViewSet

root_path = 'mte'
all_urls = [
    path(
        f'{root_path}/v1/product/list',
        CustomerViewSet.as_view(
            actions={
                'get': 'list_product',
            }
        ),
        name="List Products API"
    ),
    path(
        f'{root_path}/v1/product',
        CustomerViewSet.as_view(
            actions={
                'get': 'get_product',
            }
        ),
        name="Customer API"
    ),
    path(
        f'{root_path}/v1/product/purchase',
        CustomerViewSet.as_view(
            actions={
                'post': 'initiate_purchase',
            }
        ),
        name="Customer API"
    ),
    path(
        f'{root_path}/v1/product/payment',
        CustomerViewSet.as_view(
            actions={
                'post': 'make_payment',
            }
        ),
        name="Customer API"
    ),
]

schema_view = get_schema_view(
    openapi.Info(
        title="MTE- Backend",
        default_version='v1',
        description="",
        terms_of_service="",
    ),
    public=False,
    patterns=all_urls,
    permission_classes=[],
    generator_class=BothHttpAndHttpsSchemaGenerator,
)

urlpatterns = all_urls + [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='Documentation'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
