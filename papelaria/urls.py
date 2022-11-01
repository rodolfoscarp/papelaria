from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from cliente.views import ClienteViewSet
from vendedor.views import VendedorViewSet
from produto.views import ProdutoViewSet

router = DefaultRouter()
router.register(r'cliente', ClienteViewSet, basename='cliente')
router.register(r'vendedor', VendedorViewSet, basename='vendedor')
router.register(r'produto', ProdutoViewSet, basename='produto')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
