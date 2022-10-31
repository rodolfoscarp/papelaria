from django.contrib import admin
from .models import Cliente
from phonenumber_field.formfields import PhoneNumberField


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')


admin.site.register(Cliente, ClienteAdmin)
