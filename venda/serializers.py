from rest_framework import serializers
from .models import Venda, ItemVenda, PercentualComissao


class ItemVendaSerializer(serializers.ModelSerializer):

    percentual_comissao = serializers.FloatField(read_only=True)
    comissao = serializers.FloatField(read_only=True)
    total_produto = serializers.FloatField(read_only=True)
    valor_unitario = serializers.FloatField(
        source='produto.valor_unitario', read_only=True)
    produto_descricao = serializers.CharField(
        source='produto.descricao', read_only=True)

    class Meta:
        model = ItemVenda
        fields = [
            'quantidade', 'percentual_comissao',
            'produto', 'produto_descricao',
            'comissao', 'total_produto', 'valor_unitario',
        ]


class VendaSerializer(serializers.ModelSerializer):

    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    vendedor_nome = serializers.CharField(
        source='vendedor.nome', read_only=True)
    items = ItemVendaSerializer(many=True, required=True)

    class Meta:
        model = Venda
        fields = [
            'numero_nota', 'data_hora',
            'cliente', 'cliente_nome',
            'vendedor', 'vendedor_nome', 'items'
        ]

    def create(self, validated_data):
        items = validated_data.pop('items')

        venda = Venda.objects.create(**validated_data)

        dia_semana = venda.data_hora.weekday()

        percentual_comissao_dia_semana = PercentualComissao.objects.filter(
            dia_semana=dia_semana
        ).first()

        for item in items:
            produto = item['produto']

            percentual_comissao = produto.percentual_comissao

            if percentual_comissao_dia_semana:
                if percentual_comissao > percentual_comissao_dia_semana.maximo:
                    percentual_comissao = percentual_comissao_dia_semana.maximo
                elif percentual_comissao < percentual_comissao_dia_semana.minimo:
                    percentual_comissao = percentual_comissao_dia_semana.minimo

            ItemVenda.objects.create(
                venda=venda,
                percentual_comissao=percentual_comissao,
                **item
            )

        return venda
