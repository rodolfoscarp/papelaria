from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Vendedor
from django.forms.models import model_to_dict
from faker import Faker

fake = Faker(locale='pt_BR')


class CreateVendedorTests(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = reverse('vendedor-list')
        cls.nome = fake.name()
        cls.email = fake.email()
        cls.telefone = '(21) 99999-9999'

    def test_deve_cadastra_novo_vendedor(self):

        vendedor = dict(
            nome=self.nome,
            email=self.email,
            telefone=self.telefone,
        )

        res = self.client.post(self.url, vendedor, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(vendedor['nome'], Vendedor.objects.get().nome)
        self.assertEqual(vendedor['email'], Vendedor.objects.get().email)
        self.assertEqual(vendedor['telefone'], Vendedor.objects.get().telefone)

    def test_nao_deve_cadastrar_novo_vendedor_sem_nome(self):
        vendedor = dict(
            email=self.email,
            telefone=self.telefone,
        )

        res = self.client.post(self.url, vendedor, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_vendedor_com_nome_vazio(self):
        vendedor = dict(
            nome='',
            email=self.email,
            telefone=self.telefone,
        )

        res = self.client.post(self.url, vendedor, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_vendedor_sem_telefone(self):
        vendedor = dict(
            nome=self.nome,
            email=self.email,
        )

        res = self.client.post(self.url, vendedor, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_vendedor_com_telefone_vazio(self):
        vendedor = dict(
            nome=self.nome,
            email=self.email,
            telefone=''
        )

        res = self.client.post(self.url, vendedor, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_vendedor_com_telefone_invalido(self):
        vendedor = dict(
            nome=self.nome,
            email=self.email,
            telefone='55885588',
        )

        res = self.client.post(self.url, vendedor, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_vendedor_sem_email(self):
        vendedor = dict(
            nome=self.nome,
            email=self.email,
        )

        res = self.client.post(self.url, vendedor, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_vendedor_com_email_vazio(self):
        vendedor = dict(
            nome=self.nome,
            telefone=self.telefone,
            email=''
        )

        res = self.client.post(self.url, vendedor, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_deve_cadastrar_novo_vendedor_com_email_invalido(self):
        vendedor = dict(
            nome=self.nome,
            email='email_invalido',
            telefone=self.telefone,
        )

        res = self.client.post(self.url, vendedor, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ListVendedorTests(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('vendedor-list')

        self.vendedor1 = dict(
            nome=fake.name(),
            email=fake.email(),
            telefone='(21) 99999-9999'
        )

        self.vendedor2 = dict(
            nome=fake.name(),
            email=fake.email(),
            telefone='(22) 99999-9999'
        )

        self.vendedor3 = dict(
            nome=fake.name(),
            email=fake.email(),
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
        vendedor = Vendedor.objects.get(id=1)

        res = self.client.get(f'{self.url}1/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), model_to_dict(vendedor))


class UpdateVendedorTests(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:

        cls.url = reverse('vendedor-list')

        Vendedor.objects.create(
            nome=fake.name(),
            email=fake.email(),
            telefone='(21) 99999-9999'
        )

    def test_deve_atualizar_todos_os_campos_do_vendedor(self):

        vendedor = dict(
            nome=fake.name(),
            email=fake.email(),
            telefone='(22) 99999-9999',
        )

        res = self.client.put(self.url + '1/', vendedor, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(vendedor['nome'], Vendedor.objects.get().nome)
        self.assertEqual(
            vendedor['email'], Vendedor.objects.get().email)
        self.assertEqual(
            vendedor['telefone'], Vendedor.objects.get().telefone
        )

    def test_deve_atualizar_um_campo_do_vendedor(self):

        vendedor_update = dict(
            nome=fake.name()
        )

        res = self.client.patch(
            self.url + '1/', vendedor_update, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(vendedor_update['nome'], Vendedor.objects.get().nome)
