from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

from rest_framework.routers import DefaultRouter
from cliente.views import ClienteViewSet
from vendedor.views import VendedorViewSet, ComissaoListView
from produto.views import ProdutoViewSet
from venda.views import VendaViewSet

router = DefaultRouter()
router.register(r'cliente', ClienteViewSet, basename='cliente')
router.register(r'vendedor', VendedorViewSet, basename='vendedor')
router.register(r'produto', ProdutoViewSet, basename='produto')
router.register(r'venda', VendaViewSet, basename='venda')

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="API",
        default_version='1.0.0',
        description="API Papelaria",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comissao/', ComissaoListView.as_view(), name='comissao'),
    path('', include(router.urls)),
    path(
        'doc/', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
]
