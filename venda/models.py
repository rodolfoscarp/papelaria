from django.db import models
from cliente.models import Cliente
from vendedor.models import Vendedor
from produto.models import Produto
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Venda(models.Model):
    numero_nota = models.AutoField(primary_key=True)
    data_hora = models.DateTimeField(
        blank=False, null=False
    )

    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE,
        blank=False, null=False,
        related_name='compras'
    )

    vendedor = models.ForeignKey(
        Vendedor, on_delete=models.CASCADE,
        blank=False, null=False,
        related_name='vendas'
    )

    def __str__(self) -> str:
        return super().__str__()


class ItemVenda(models.Model):
    venda = models.ForeignKey(
        Venda, on_delete=models.CASCADE,
        blank=False, null=False,
        related_name='items'
    )

    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE,
        blank=False, null=False,
        related_name='items'
    )

    quantidade = models.PositiveIntegerField(blank=False, null=False)
    percentual_comissao = models.FloatField(blank=False, null=False, validators=[
        MinValueValidator(0.01), MaxValueValidator(0.1)
    ])

    @property
    def comissao(self):
        return self.total_produto * self.percentual_comissao

    @property
    def total_produto(self):
        return self.quantidade * self.produto.valor_unitario

    def __str__(self) -> str:
        return super().__str__()


class PercentualComissao(models.Model):
    class DiaSemana(models.IntegerChoices):
        SEGUNDA = 0
        TERCA = 1
        QUARTA = 2
        QUINTA = 3
        SEXTA = 4
        SABADO = 5
        DOMINGO = 6

    dia_semana = models.IntegerField(
        unique=True, choices=DiaSemana.choices,
        null=False
    )

    minimo = models.FloatField(validators=[
        MinValueValidator(0.01), MaxValueValidator(0.1)
    ], null=True)

    maximo = models.FloatField(validators=[
        MinValueValidator(0.01), MaxValueValidator(0.1)
    ], null=True)

    def clean(self) -> None:
        if self.minimo > self.maximo:
            raise ValidationError(
                {'minimo': 'Valor mínimo deve ser maior que o máximo.'})
