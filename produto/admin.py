from django.contrib import admin
from .models import Produto


class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo', 'descricao',
        'valor_unitario', 'percentual_comissao'
    )


admin.site.register(Produto, ProdutoAdmin)
