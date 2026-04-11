from django.contrib import admin
from .models import Licenciatura, Docente, UnidadeCurricular, Competencia


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


@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'ano', 'semestre', 'ects')
    search_fields = ('nome', 'codigo')
    list_filter = ('ano', 'semestre', 'licenciaturas')
    filter_horizontal = ('licenciaturas', 'docentes')


@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'nivel')
    search_fields = ('nome',)
    list_filter = ('tipo', 'nivel')