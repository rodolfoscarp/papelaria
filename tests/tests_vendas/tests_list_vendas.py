from rest_framework.test import APITestCase
from django.urls import reverse
from ..dummies import make_venda
from rest_framework import status
from venda.models import Venda, ItemVenda
from datetime import datetime

url = reverse('venda-list')


class ListVendaTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for _ in range(5):
            make_venda()

    def test_deve_listar_todas_as_vendas_cadastrados(self):
        vendas = self.client.get(url)

        vendas.json()

        vendas_result = vendas.json()['results']

        self.assertEqual(vendas.status_code, status.HTTP_200_OK)
        self.assertEqual(len(vendas_result), 5)

    def test_deve_listar_uma_venda(self):
        venda = Venda.objects.first()
        item_venda = ItemVenda.objects.filter(venda=venda).first()

        pk = venda.pk

        res = self.client.get(f'{url}{pk}/')

        venda_result = res.json()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(venda_result['numero_nota'], venda.numero_nota)
        self.assertEqual(datetime.fromisoformat(
            venda_result['data_hora']), venda.data_hora)
        self.assertEqual(venda_result['cliente'], venda.cliente.pk)
        self.assertEqual(venda_result['cliente_nome'], venda.cliente.nome)
        self.assertEqual(venda_result['vendedor'], venda.vendedor.pk)
        self.assertEqual(venda_result['vendedor_nome'], venda.vendedor.nome)
        self.assertEqual(venda_result['items'][0]
                         ['quantidade'], item_venda.quantidade)
        self.assertEqual(
            venda_result['items'][0]['percentual_comissao'], item_venda.percentual_comissao)
        self.assertEqual(venda_result['items'][0]
                         ['produto'], item_venda.produto.pk)
        self.assertEqual(
            venda_result['items'][0]['produto_descricao'], item_venda.produto.descricao)
        self.assertEqual(
            venda_result['items'][0]['comissao'], item_venda.comissao)
        self.assertEqual(venda_result['items'][0]
                         ['total_produto'], item_venda.total_produto)
        self.assertEqual(
            venda_result['items'][0]['valor_unitario'], item_venda.produto.valor_unitario)
