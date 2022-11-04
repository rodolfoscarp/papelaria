from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Produto
from django.forms.models import model_to_dict


class CreateProdutoTests(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('produto-list')

    def test_deve_cadastrar_novo_produto(self):
        produto = {
            'valor_unitario': 10.00,
            'percentual_comissao': 0.1,
            'descricao': 'Produto1'
        }

        res = self.client.post(self.url, produto, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(produto['descricao'], Produto.objects.get().descricao)
        self.assertEqual(
            produto['valor_unitario'], Produto.objects.get().valor_unitario)
        self.assertEqual(
            produto['percentual_comissao'], Produto.objects.get().percentual_comissao)

    def test_nao_deve_cadastrar_novo_produto_sem_descricao(self):

        produto = {
            'valor_unitario': 10.00,
            'percentual_comissao': 0.02,
        }

        res = self.client.post(self.url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_com_descricao_vazia(self):

        produto = {
            'valor_unitario': 10.00,
            'percentual_comissao': 0.02,
            'descricao': ''
        }

        res = self.client.post(self.url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_sem_valor_unitario(self):
        produto = {
            'percentual_comissao': 0.02,
            'descricao': 'Produto1'
        }

        res = self.client.post(self.url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_com_valor_unitario_menor_que_um(self):
        produto = {
            'valor_unitario': 0,
            'percentual_comissao': 0.02,
            'descricao': 'Produto1'
        }

        res = self.client.post(self.url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_sem_percentual_comissao(self):
        produto = {
            'valor_unitario': 0,
            'descricao': ''
        }

        res = self.client.post(self.url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_com_percentual_comissao_menor_que_um_por_centor(self):
        produto = {
            'valor_unitario': 10.00,
            'percentual_comissao': 0,
            'descricao': 'Produto1'}

        res = self.client.post(self.url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_com_percentual_comissao_maior_que_dez_por_centor(self):
        produto = {
            'valor_unitario': 10.00,
            'percentual_comissao': 0.2,
            'descricao': 'Produto1'
        }

        res = self.client.post(self.url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ListProdutoTests(APITestCase):
    pass


class UpdateProdutoTests(APITestCase):
    pass
