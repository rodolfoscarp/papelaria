from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Vendedor(models.Model):
    nome = models.CharField(max_length=80, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    telefone = PhoneNumberField(blank=False, null=False)

    def __str__(self) -> str:
        return self.nome