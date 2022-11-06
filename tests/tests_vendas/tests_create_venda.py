from rest_framework.test import APIClient
from django.urls import reverse
from ..dummies import make_cliente, make_produto, make_vendedor, make_percentual
from rest_framework import status
from venda.models import Venda, ItemVenda
from datetime import datetime
import pytest


@pytest.mark.django_db
def test_deve_cadastrar_uma_nova_venda():
    url = reverse('venda-list')
    api_client = APIClient()

    quantidade_produto = 10
    valor_unitario_produto = 100
    percentual_comissao_produto = 0.01

    cliente = make_cliente()
    produto = make_produto(
        valor_unitario=valor_unitario_produto,
        percentual_comissao=percentual_comissao_produto
    )
    vendedor = make_vendedor()

    venda_req = {
        "data_hora": "2022-11-07T00:00:00-03:00",
        "cliente": cliente.pk,
        "vendedor": vendedor.pk,
        "items": [
                {
                    "quantidade": quantidade_produto,
                    "produto": produto.codigo
                }
        ]
    }

    res = api_client.post(url, data=venda_req, format='json')

    venda = Venda.objects.get()
    item_venda = ItemVenda.objects.get()

    assert res.status_code == status.HTTP_201_CREATED
    assert venda.data_hora == datetime.fromisoformat(
        venda_req['data_hora']
    )

    assert venda.cliente.pk == cliente.pk
    assert venda.vendedor.pk == vendedor.pk
    assert item_venda.venda.pk == venda.pk
    assert item_venda.quantidade == quantidade_produto
    assert item_venda.total_produto == quantidade_produto * valor_unitario_produto
    assert item_venda.comissao == \
        quantidade_produto * valor_unitario_produto * percentual_comissao_produto
    assert item_venda.percentual_comissao == percentual_comissao_produto


@pytest.mark.django_db
def test_deve_cadastrar_item_com_percetual_minimo_do_dia_da_semana():
    url = reverse('venda-list')
    api_client = APIClient()

    quantidade_produto = 10
    valor_unitario_produto = 100
    percentual_comissao_produto = 0.02
    percentual_minimo = 0.05

    # Cria Configuração minimo percentual de comissão para 5%
    # as segundas-feiras
    make_percentual(0, minimo=percentual_minimo)

    cliente = make_cliente()
    produto = make_produto(
        valor_unitario=valor_unitario_produto,
        percentual_comissao=percentual_comissao_produto
    )
    vendedor = make_vendedor()

    venda_req = {
        "data_hora": "2022-10-31T00:00:00-03:00",
        "cliente": cliente.pk,
        "vendedor": vendedor.pk,
        "items": [
                {
                    "quantidade": quantidade_produto,
                    "produto": produto.codigo
                }
        ]
    }

    res = api_client.post(url, data=venda_req, format='json')

    item_venda = ItemVenda.objects.get()

    assert res.status_code == status.HTTP_201_CREATED
    assert item_venda.percentual_comissao == percentual_minimo
    assert item_venda.total_produto == quantidade_produto * valor_unitario_produto
    assert item_venda.comissao == \
        quantidade_produto * valor_unitario_produto * percentual_minimo


@pytest.mark.django_db
def test_deve_cadastrar_item_com_percetual_maximo_do_dia_da_semana():
    url = reverse('venda-list')
    api_client = APIClient()

    quantidade_produto = 10
    valor_unitario_produto = 100
    percentual_comissao_produto = 0.09
    percentual_maximo = 0.08

    # Cria Configuração maximo percentual de comissão para 8%
    # as segundas-feiras
    make_percentual(0, maximo=percentual_maximo)

    cliente = make_cliente()
    produto = make_produto(
        valor_unitario=valor_unitario_produto,
        percentual_comissao=percentual_comissao_produto
    )
    vendedor = make_vendedor()

    venda_req = {
        "data_hora": "2022-10-31T00:00:00-03:00",
        "cliente": cliente.pk,
        "vendedor": vendedor.pk,
        "items": [
                {
                    "quantidade": quantidade_produto,
                    "produto": produto.codigo
                }
        ]
    }

    res = api_client.post(url, data=venda_req, format='json')

    item_venda = ItemVenda.objects.get()

    assert res.status_code == status.HTTP_201_CREATED
    assert item_venda.percentual_comissao == percentual_maximo
    assert item_venda.total_produto == quantidade_produto * valor_unitario_produto
    assert item_venda.comissao == \
        quantidade_produto * valor_unitario_produto * percentual_maximo
