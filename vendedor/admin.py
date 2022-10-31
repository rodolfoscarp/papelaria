from django.contrib import admin
from .models import Vendedor
from phonenumber_field.formfields import PhoneNumberField


class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')


admin.site.register(Vendedor, VendedorAdmin)
