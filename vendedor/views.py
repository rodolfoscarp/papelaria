from rest_framework import viewsets
from .serializers import VendedorSerializer, ComissaoSerializer
from .models import Vendedor
from rest_framework.generics import ListAPIView


class VendedorViewSet(viewsets.ModelViewSet):
    serializer_class = VendedorSerializer
    queryset = Vendedor.objects.all().order_by('-pk')


class ComissaoListView(ListAPIView):

    serializer_class = ComissaoSerializer
    queryset = Vendedor.objects.all().order_by('-pk')
