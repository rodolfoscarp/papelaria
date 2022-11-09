from rest_framework import viewsets, mixins
from .serializers import VendedorSerializer
from .models import Vendedor
from .serializers import ComissaoSerializer
from django_filters import rest_framework as filters


class VendedorViewSet(viewsets.ModelViewSet):
    serializer_class = VendedorSerializer
    queryset = Vendedor.objects.all().order_by('-pk')


class ComissaoFilter(filters.FilterSet):
    vendas__data_hora__gte = filters.DateTimeFilter(
        field_name="vendas__data_hora", lookup_expr='date__lte')
    vendas__data_hora__lte = filters.DateTimeFilter(
        field_name="vendas__data_hora", lookup_expr='date__lte')

    class Meta:
        model = Vendedor
        fields = ['vendas__data_hora__gte', 'vendas__data_hora__lte']


class ComissaoListView(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = ComissaoSerializer
    filterset_class = ComissaoFilter
    queryset = Vendedor.objects.all().order_by('-pk')
    filter_backends = [filters.DjangoFilterBackend]
