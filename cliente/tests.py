from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Cliente
from django.forms.models import model_to_dict


def make_cliente(**kwargs):

    return {
        'nome': kwargs.get('nome', 'Cliente1'),
        'email': kwargs.get('email', 'cliente1@cliente.com.br'),
        'telefone': kwargs.get('telefone', '(24) 99999-9999')
    }


class CreateClienteTests(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('cliente-list')

    def test_deve_cadastra_novo_cliente(self):
        cliente_data = make_cliente()

        res = self.client.post(self.url, cliente_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual('Cliente1', Cliente.objects.get().nome)
        self.assertEqual('cliente1@cliente.com.br',
                         Cliente.objects.get().email)
        self.assertEqual('(24) 99999-9999', Cliente.objects.get().telefone)

    def test_nao_deve_cadastrar_novo_cliente_sem_nome(self):
        cliente_data = make_cliente(nome=None)

        res = self.client.post(self.url, cliente_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_sem_telefone(self):
        cliente_data = make_cliente(telefone=None)

        res = self.client.post(self.url, cliente_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_sem_email(self):
        cliente_data = make_cliente(email=None)

        res = self.client.post(self.url, cliente_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_com_email_invalido(self):
        cliente_data = make_cliente(email='cliente.cliente.com.br')

        res = self.client.post(self.url, cliente_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_com_telefone_invalido(self):
        cliente_data = make_cliente(telefone='55885588')

        res = self.client.post(self.url, cliente_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ListClienteTests(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('cliente-list')
        self.cliente1 = dict(
            nome='Cliente1', email='cliente1@cliente.com.br',
            telefone='(21) 99999-9999'
        )

        self.cliente2 = dict(
            nome='Cliente2', email='cliente2@cliente.com.br',
            telefone='(22) 99999-9999'
        )

        self.cliente3 = dict(
            nome='Cliente3', email='cliente3@cliente.com.br',
            telefone='(23) 99999-9999'
        )

        Cliente.objects.create(**self.cliente1)
        Cliente.objects.create(**self.cliente2)
        Cliente.objects.create(**self.cliente3)

    def test_deve_listar_todos_os_clientes_cadastrados(self):
        clientes = self.client.get(self.url)

        clientes.json()

        self.assertEqual(clientes.status_code, status.HTTP_200_OK)
        self.assertEqual(len(clientes.json()), 3)

    def test_deve_listar_um_cliente(self):
        cliente1 = Cliente.objects.get(id=1)

        res = self.client.get(f'{self.url}1/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), model_to_dict(cliente1))


class UpdateClienteTests(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('cliente-list')
        self.cliente1 = make_cliente()

        Cliente.objects.create(**self.cliente1)

    def test_deve_atualizar_todos_os_campos_do_cliente(self):

        cliente_data = make_cliente(
            nome='Cliente2', email='cliente2@cliente.com.br',
            telefone='(22) 99999-9999'
        )

        res = self.client.put(self.url + '1/', cliente_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual('Cliente2', Cliente.objects.get().nome)
        self.assertEqual('cliente2@cliente.com.br',
                         Cliente.objects.get().email)
        self.assertEqual('(22) 99999-9999', Cliente.objects.get().telefone)

    def test_deve_atualizar_um_campo_do_cliente(self):

        res = self.client.patch(self.url + '1/', {'nome': 'Cliente3'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual('Cliente3', Cliente.objects.get().nome)
