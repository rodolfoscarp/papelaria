from rest_framework import viewsets
from .serializers import VendedorViewSet, ComissaoSerializer
from .models import Vendedor
from rest_framework.generics import ListAPIView


class VendedorViewSet(viewsets.ModelViewSet):
    serializer_class = VendedorViewSet
    queryset = Vendedor.objects.all()


class ComissaoListView(ListAPIView):

    serializer_class = ComissaoSerializer
    queryset = Vendedor.objects.all()

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['category', 'in_stock']
