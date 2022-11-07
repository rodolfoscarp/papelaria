from django.urls import reverse
from rest_framework.test import APITestCase
from ..dummies import make_venda
from rest_framework import status
from venda.models import ItemVenda, Venda

url = reverse('venda-list')


class DeleteVendedorTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        make_venda()

    def test_deve_deletar_um_vendedor(self):
        res_delete = self.client.delete(url + '1/')

        vendas = Venda.objects.all()
        items_venda = ItemVenda.objects.all()

        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(vendas), 0)
        self.assertEqual(len(items_venda), 0)
