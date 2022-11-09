from rest_framework import serializers
from .models import Vendedor
from venda.models import Venda, ItemVenda


class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'


class ComissaoVendaItemSerializer(serializers.ModelSerializer):

    quantidade = serializers.IntegerField()
    percentual_comissao = serializers.FloatField()
    produto = serializers.CharField(source='produto.descricao')
    valor_unitario = serializers.FloatField(source='produto.valor_unitario')

    class Meta:
        model = ItemVenda
        fields = [
            'quantidade', 'percentual_comissao',
            'produto', 'valor_unitario'
        ]


class ComissaoVendaSerializer(serializers.ModelSerializer):
    data_hora = serializers.DateTimeField()
    items = ComissaoVendaItemSerializer(many=True)

    class Meta:
        model = Venda
        fields = ['data_hora', 'items']


class ComissaoSerializer(serializers.ModelSerializer):

    pk = serializers.IntegerField()
    nome = serializers.CharField()
    vendas = ComissaoVendaSerializer(many=True)

    class Meta:
        model = Vendedor
        fields = ['pk', 'nome', 'vendas']
