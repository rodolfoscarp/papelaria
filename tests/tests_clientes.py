from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from cliente.models import Cliente
from django.forms.models import model_to_dict
from .dummies import make_cliente

from faker import Faker

fake = Faker(locale='pt_BR')


url = reverse('cliente-list')


class CreateClienteTests(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.nome = fake.name()
        cls.email = fake.email()
        cls.telefone = '(21) 99999-9999'

    def test_deve_cadastra_novo_cliente(self):
        cliente = dict(
            nome=self.nome,
            email=self.email,
            telefone=self.telefone,
        )

        res = self.client.post(url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(cliente['nome'], Cliente.objects.get().nome)
        self.assertEqual(cliente['email'], Cliente.objects.get().email)
        self.assertEqual(cliente['telefone'], Cliente.objects.get().telefone)

    def test_nao_deve_cadastrar_novo_cliente_sem_nome(self):
        cliente = dict(
            email=self.email,
            telefone=self.telefone,
        )

        res = self.client.post(url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_nome_vazio(self):
        cliente = dict(
            nome='',
            email=self.email,
            telefone=self.telefone,
        )

        res = self.client.post(url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_sem_telefone(self):
        cliente = dict(
            nome=self.nome,
            email=self.email,
        )

        res = self.client.post(url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_com_telefone_vazio(self):
        cliente = dict(
            telefone='',
            nome=self.nome,
            email=self.email,
        )

        res = self.client.post(url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_com_telefone_invalido(self):
        cliente = dict(
            nome=self.nome,
            email=self.email,
            telefone='999999999'
        )

        res = self.client.post(url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_sem_email(self):
        cliente = dict(
            nome=self.nome,
            telefone=self.telefone
        )

        res = self.client.post(url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_com_email_vazio(self):
        cliente = dict(
            nome=self.nome,
            telefone=self.telefone,
            email=''
        )

        res = self.client.post(url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_cliente_com_email_invalido(self):
        cliente = dict(
            nome=self.nome,
            email='cliente1.cliente.com.br',
            telefone=self.telefone
        )

        res = self.client.post(url, cliente, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ListClienteTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for _ in range(5):
            make_cliente()

    def test_deve_listar_todos_os_clientes_cadastrados(self):
        clientes = self.client.get(url)

        clientes.json()

        clientes_result = clientes.json()['results']

        self.assertEqual(clientes.status_code, status.HTTP_200_OK)
        self.assertEqual(len(clientes_result), 5)

    def test_deve_listar_um_cliente(self):
        cliente1 = Cliente.objects.first()

        pk = cliente1.pk

        res = self.client.get(f'{url}{pk}/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), model_to_dict(cliente1))


class UpdateClienteTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.cliente = make_cliente(
            telefone='(24) 99999-9999'
        )

    def test_deve_atualizar_todos_os_campos_do_cliente(self):

        pk = self.cliente.pk

        cliente_update = dict(
            nome=fake.name(),
            email=fake.email(),
            telefone='(22) 99999-9999',
        )

        res = self.client.put(url + f'{pk}/', cliente_update)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(cliente_update['nome'], Cliente.objects.get().nome)
        self.assertEqual(
            cliente_update['email'],
            Cliente.objects.get().email)
        self.assertEqual(
            cliente_update['telefone'],
            Cliente.objects.get().telefone)

    def test_deve_atualizar_um_campo_do_cliente(self):

        pk = self.cliente.pk

        cliente_update = dict(
            nome=fake.name()
        )

        res = self.client.patch(url + f'{pk}/', cliente_update)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            cliente_update['nome'],
            Cliente.objects.get().nome
        )


class DeleteClienteTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.cliente = make_cliente()

    def test_deve_deletar_um_cliente(self):

        pk = self.cliente.pk
        res = self.client.delete(url + f'{pk}/')

        clientes = Cliente.objects.all()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(clientes), 0)
