from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Cliente


class ClienteApiTests(APITestCase):
    def test_deve_cadastra_novo_cliente(self):
        url = reverse('cliente-list')
        data = {
            'nome': 'Cliente1',
            'email': 'cliente@cliente.com.br',
            'telefone': '(24) 99999-9999'
        }

        res = self.client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual('Cliente1', Cliente.objects.get().nome)
        self.assertEqual('cliente@cliente.com.br', Cliente.objects.get().email)
        self.assertEqual('(24) 99999-9999', Cliente.objects.get().telefone)
