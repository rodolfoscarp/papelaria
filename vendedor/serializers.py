from rest_framework import serializers
from .models import Vendedor
from venda.models import Venda
from django.db.models import Sum, F


class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'


class ComissaoSerializer(serializers.ModelSerializer):
    cod = serializers.IntegerField(source='pk')
    nome = serializers.CharField()
    total_vendas = serializers.SerializerMethodField('get_total_vendas')
    total_comissao = serializers.SerializerMethodField(
        'get_total_comissao')

    class Meta:
        model = Vendedor
        fields = ['cod', 'nome', 'total_vendas', 'total_comissao']

    def get_total_vendas(self, obj):
        vendas = Venda.objects.filter(vendedor=obj.pk)
        return vendas.count()

    def get_total_comissao(self, obj):
        total_comissao = Venda.objects.filter(vendedor=obj.pk).annotate(comissao=F(
            'items__produto__valor_unitario') * F('items__quantidade') * F('items__percentual_comissao')).aggregate(
                Sum('comissao'))

        return total_comissao['comissao__sum']
