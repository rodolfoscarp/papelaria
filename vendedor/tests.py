from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Vendedor
from django.forms.models import model_to_dict


def make_vendedor(**kwargs):

    return {
        'nome': kwargs.get('nome', 'Vendedor1'),
        'email': kwargs.get('email', 'vendedor1@vendedor.com.br'),
        'telefone': kwargs.get('telefone', '(24) 99999-9999')
    }


class CreateVendedorTests(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('vendedor-list')

    def test_deve_cadastra_novo_vendedor(self):
        vendedor_data = make_vendedor()

        res = self.client.post(self.url, vendedor_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual('Vendedor1', Vendedor.objects.get().nome)
        self.assertEqual('vendedor1@vendedor.com.br',
                         Vendedor.objects.get().email)
        self.assertEqual('(24) 99999-9999', Vendedor.objects.get().telefone)

    def test_nao_deve_cadastrar_novo_vendedor_sem_nome(self):
        vendedor_data = make_vendedor(nome=None)

        res = self.client.post(self.url, vendedor_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_vendedor_sem_telefone(self):
        vendedor_data = make_vendedor(telefone=None)

        res = self.client.post(self.url, vendedor_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_vendedor_sem_email(self):
        vendedor_data = make_vendedor(email=None)

        res = self.client.post(self.url, vendedor_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_vendedor_com_email_invalido(self):
        vendedor_data = make_vendedor(email='.cliente.com.br')

        res = self.client.post(self.url, vendedor_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_vendedor_com_telefone_invalido(self):
        vendedor_data = make_vendedor(telefone='55885588')

        res = self.client.post(self.url, vendedor_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ListVendedorTests(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('vendedor-list')
        self.vendedor1 = dict(
            nome='Vendedor1', email='vendedor1@vendedor.com.br',
            telefone='(21) 99999-9999'
        )

        self.vendedor2 = dict(
            nome='Vendedor2', email='2@vendedor.com.br',
            telefone='(22) 99999-9999'
        )

        self.vendedor3 = dict(
            nome='Vendedor3', email='3@vendedor.com.br',
            telefone='(23) 99999-9999'
        )

        Vendedor.objects.create(**self.vendedor1)
        Vendedor.objects.create(**self.vendedor2)
        Vendedor.objects.create(**self.vendedor3)

    def test_deve_listar_todos_os_vendedores_cadastrados(self):
        vendedores = self.client.get(self.url)

        vendedores.json()

        self.assertEqual(vendedores.status_code, status.HTTP_200_OK)
        self.assertEqual(len(vendedores.json()), 3)

    def test_deve_listar_um_vendedor(self):
        vendedor1 = Vendedor.objects.get(id=1)

        res = self.client.get(f'{self.url}1/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), model_to_dict(vendedor1))


class UpdateVendedorTests(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('vendedor-list')
        self.vendedor1 = make_vendedor()

        Vendedor.objects.create(**self.vendedor1)

    def test_deve_atualizar_todos_os_campos_do_vendedor(self):

        vendedor_data = make_vendedor(
            nome='Vendedor2', email='vendedor2@vendedor.com.br',
            telefone='(22) 99999-9999'
        )

        res = self.client.put(self.url + '1/', vendedor_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual('Vendedor2', Vendedor.objects.get().nome)
        self.assertEqual('vendedor2@vendedor.com.br',
                         Vendedor.objects.get().email)
        self.assertEqual('(22) 99999-9999', Vendedor.objects.get().telefone)

    def test_deve_atualizar_um_campo_do_vendedor(self):

        res = self.client.patch(self.url + '1/', {'nome': 'vendedor3'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual('vendedor3', Vendedor.objects.get().nome)
