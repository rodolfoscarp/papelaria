from rest_framework import viewsets
from .serializers import ProdutoSerializer
from .models import Produto


class ProdutoViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoSerializer
    queryset = Produto.objects.all().order_by('-pk')
