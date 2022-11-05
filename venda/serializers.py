from rest_framework import serializers
from .models import Venda


class ProdutoVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = ['quantidade', 'percentual_comissao']


class VendaSerializer(serializers.ModelSerializer):

    produtos = ProdutoVendaSerializer(many=True, read_only=True)

    class Meta:
        model = Venda
        fields = [
            'numero_nota', 'data_hora',
            'cliente', 'vendedor', 'produtos'
        ]
