from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Produto(models.Model):
    codigo = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=80, blank=False, null=False)
    valor_unitario = models.FloatField(blank=False, null=False, validators=[
        MinValueValidator(0.01)
    ])
    percentual_comissao = models.FloatField(blank=False, null=False, validators=[
        MinValueValidator(0.01), MaxValueValidator(0.1)
    ])

    def __str__(self) -> str:
        return self.descricao
