from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from produto.models import Produto
from django.forms.models import model_to_dict
from .dummies import make_produto

url = reverse('produto-list')


class CreateProdutoTests(APITestCase):
    def test_deve_cadastrar_novo_produto(self):
        produto = {
            'valor_unitario': 10.00,
            'percentual_comissao': 0.1,
            'descricao': 'Produto1'
        }

        res = self.client.post(url, produto, format='json')

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

        res = self.client.post(url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_com_descricao_vazia(self):

        produto = {
            'valor_unitario': 10.00,
            'percentual_comissao': 0.02,
            'descricao': ''
        }

        res = self.client.post(url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_sem_valor_unitario(self):
        produto = {
            'percentual_comissao': 0.02,
            'descricao': 'Produto1'
        }

        res = self.client.post(url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_com_valor_unitario_menor_que_um(self):
        produto = {
            'valor_unitario': 0,
            'percentual_comissao': 0.02,
            'descricao': 'Produto1'
        }

        res = self.client.post(url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_sem_percentual_comissao(self):
        produto = {
            'valor_unitario': 0,
            'descricao': ''
        }

        res = self.client.post(url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_com_percentual_comissao_menor_que_um_por_centor(self):
        produto = {
            'valor_unitario': 10.00,
            'percentual_comissao': 0,
            'descricao': 'Produto1'}

        res = self.client.post(url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_produto_com_percentual_comissao_maior_que_dez_por_centor(self):
        produto = {
            'valor_unitario': 10.00,
            'percentual_comissao': 0.2,
            'descricao': 'Produto1'
        }

        res = self.client.post(url, produto)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ListProdutoTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for _ in range(5):
            make_produto()

    def test_deve_listar_todos_os_produtos_cadastrados(self):
        produtos = self.client.get(url)

        produtos_result = produtos.json()['results']

        self.assertEqual(produtos.status_code, status.HTTP_200_OK)
        self.assertEqual(len(produtos_result), 5)

    def test_deve_listar_um_produto(self):
        produto = Produto.objects.first()

        pk = produto.pk

        res = self.client.get(f'{url}{pk}/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), model_to_dict(produto))


class UpdateProdutoTests(APITestCase):
    pass


class DeleteProdutoTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.produto = make_produto()

    def test_deve_deletar_um_produto(self):

        pk = self.produto.pk

        res = self.client.delete(url + f'{pk}/')

        produtos = Produto.objects.all()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(produtos), 0)
