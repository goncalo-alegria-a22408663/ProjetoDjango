from django.contrib import admin
from .models import Licenciatura, Docente


@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome', 'instituicao', 'duracao_anos', 'total_ects')
    search_fields = ('nome', 'sigla', 'instituicao')
    list_filter = ('instituicao', 'duracao_anos')


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'habilitacao', 'regime_contrato')
    search_fields = ('nome',)
    list_filter = ('habilitacao', 'regime_contrato')