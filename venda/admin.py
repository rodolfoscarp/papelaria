from django.contrib import admin
from .models import PercentualComissao


class PercentualComissaoAdmin(admin.ModelAdmin):
    list_display = ('dia_semana', 'minimo', 'maximo')
    list_editable = ('minimo', 'maximo')


admin.site.register(PercentualComissao, PercentualComissaoAdmin)
