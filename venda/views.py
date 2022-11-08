from rest_framework import viewsets
from .models import Venda
from .serializers import VendaSerializer


class VendaViewSet(viewsets.ModelViewSet):
    serializer_class = VendaSerializer
    queryset = Venda.objects.all().order_by('-pk')
