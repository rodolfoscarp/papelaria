from vendedor.models import Vendedor
from cliente.models import Cliente
from produto.models import Produto
from ..models import Venda, ItemVenda, PercentualComissao
from faker import Faker
fake = Faker(locale='pt_BR')
from datetime import datetime


def fake_telefone():
    phone = fake.msisdn()

    return '({}) {}-{}'.format(
        phone[2:4],
        phone[4:9],
        phone[9:],
    )


def make_produto(
    descricao=None,
    valor_unitario=None,
    percentual_comissao=None
):

    if not descricao:
        descricao = 'Produto1'

    if not valor_unitario:
        valor_unitario = fake.pyfloat(
            left_digits=2, right_digits=2,
            positive=True
        )

    if not percentual_comissao:
        percentual_comissao = fake.pyfloat(
            left_digits=0, right_digits=2,
            positive=True, min_value=0.01,
            max_value=0.10
        )

    return Produto.objects.create(
        descricao=descricao,
        valor_unitario=valor_unitario,
        percentual_comissao=percentual_comissao,
    )


def make_cliente(
    nome=None,
    email=None,
    telefone=None
):

    if not nome:
        nome = fake.name

    if not email:
        email = fake.email

    if not telefone:
        telefone = fake_telefone()

    return Cliente.objects.create(
        nome=nome,
        email=email,
        telefone=telefone
    )


def make_vendedor(
    nome=None,
    email=None,
    telefone=None
):
    if not nome:
        nome = fake.name

    if not email:
        email = fake.email

    if not telefone:
        telefone = fake_telefone()

    return Vendedor.objects.create(
        nome=nome,
        email=email,
        telefone=telefone
    )


def make_item_venda(
        venda,
        produto=None,
        quantidade=None,
        percentual_comissao=None
):

    if not produto:
        produto = make_produto()

    if not quantidade:
        quantidade = fake.pyint(min_value=0, max_value=10)

    if not percentual_comissao:
        percentual_comissao = produto.percentual_comissao

    if not valor_unitario:
        valor_unitario = fake.pyfloat(
            left_digits=2, right_digits=2,
            positive=True
        ),

    return ItemVenda.objects.create(
        venda,
        produto,
        quantidade,
        percentual_comissao,
    )


def make_percentual(
    dia_semana,
    minimo=0.01,
    maximo=0.1
):

    percent_comissao_seg_feira = PercentualComissao.objects.create(
        dia_semana=dia_semana,
        minimo=minimo,
        maximo=maximo,
    )


def make_venda(
    data_hora=None,
    cliente=None,
    vendedor=None,
    itens=None
):

    if not data_hora:
        data_hora = datetime.now()

    if not cliente:
        cliente = make_cliente()

    if not vendedor:
        vendedor = make_vendedor()

    venda = Venda.objects.create(
        data_hora=data_hora,
        cliente=cliente,
        vendedor=vendedor
    )

    if not itens:
        make_item_venda(venda)
        make_item_venda(venda)
        make_item_venda(venda)

    return venda
