from django.contrib import admin
from .models import Cliente
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')


admin.site.register(Cliente, ClienteAdmin)
