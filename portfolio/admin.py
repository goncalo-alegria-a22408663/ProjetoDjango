from django.contrib import admin
from .models import Licenciatura


@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome', 'instituicao', 'duracao_anos', 'total_ects')
    search_fields = ('nome', 'sigla', 'instituicao')
    list_filter = ('instituicao', 'duracao_anos')