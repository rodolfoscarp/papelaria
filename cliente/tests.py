from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Cliente
from django.forms.models import model_to_dict

from faker import Faker

fake = Faker(locale='pt_BR')


class CreateClienteTests(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = reverse('cliente-list')
        cls.nome = fake.name()
        cls.email = fake.email()
        cls.telefone = '(21) 99999-9999'

    def test_deve_cadastra_novo_cliente(self):
        cliente = dict(
            nome=self.nome,
            email=self.email,
            telefone=self.telefone,
        )

        res = self.client.post(self.url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(cliente['nome'], Cliente.objects.get().nome)
        self.assertEqual(cliente['email'], Cliente.objects.get().email)
        self.assertEqual(cliente['telefone'], Cliente.objects.get().telefone)

    def test_nao_deve_cadastrar_novo_cliente_sem_nome(self):
        cliente = dict(
            email=self.email,
            telefone=self.telefone,
        )

        res = self.client.post(self.url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_nome_vazio(self):
        cliente = dict(
            nome='',
            email=self.email,
            telefone=self.telefone,
        )

        res = self.client.post(self.url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_sem_telefone(self):
        cliente = dict(
            nome=self.nome,
            email=self.email,
        )

        res = self.client.post(self.url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_com_telefone_vazio(self):
        cliente = dict(
            telefone='',
            nome=self.nome,
            email=self.email,
        )

        res = self.client.post(self.url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_com_telefone_invalido(self):
        cliente = dict(
            nome=self.nome,
            email=self.email,
            telefone='999999999'
        )

        res = self.client.post(self.url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_sem_email(self):
        cliente = dict(
            nome=self.nome,
            telefone=self.telefone
        )

        res = self.client.post(self.url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_com_email_vazio(self):
        cliente = dict(
            nome=self.nome,
            telefone=self.telefone,
            email=''
        )

        res = self.client.post(self.url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_com_email_invalido(self):
        cliente = dict(
            nome=self.nome,
            email='cliente1.cliente.com.br',
            telefone=self.telefone
        )

        res = self.client.post(self.url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ListClienteTests(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('cliente-list')
        self.cliente1 = dict(
            nome=fake.name(),
            email=fake.email(),
            telefone='(21) 99999-9999'
        )

        self.cliente2 = dict(
            nome=fake.name(),
            email=fake.email(),
            telefone='(22) 99999-9999'
        )

        self.cliente3 = dict(
            nome=fake.name(),
            email=fake.email(),
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

        cliente1 = dict(
            nome='Cliente1',
            email='cliente1@cliente.com.br',
            telefone='(24) 99999-9999'
        )

        Cliente.objects.create(**cliente1)

    def test_deve_atualizar_todos_os_campos_do_cliente(self):

        cliente_update = dict(
            nome=fake.name(),
            email=fake.email(),
            telefone='(22) 99999-9999',
        )

        res = self.client.put(self.url + '1/', cliente_update)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(cliente_update['nome'], Cliente.objects.get().nome)
        self.assertEqual(cliente_update['email'],
                         Cliente.objects.get().email)
        self.assertEqual(cliente_update['telefone'],
                         Cliente.objects.get().telefone)

    def test_deve_atualizar_um_campo_do_cliente(self):

        cliente_update = dict(
            nome=fake.name()
        )

        res = self.client.patch(self.url + '1/', cliente_update)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(cliente_update['nome'],
                         Cliente.objects.get().nome)
