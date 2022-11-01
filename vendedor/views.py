from rest_framework import viewsets
from .serializers import VendedorViewSet
from .models import Vendedor


class VendedorViewSet(viewsets.ModelViewSet):
    serializer_class = VendedorViewSet
    queryset = Vendedor.objects.all()
