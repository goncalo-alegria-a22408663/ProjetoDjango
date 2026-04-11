from django.contrib import admin
from .models import Licenciatura, Docente, UnidadeCurricular, Competencia, Tecnologia, TFC, Projeto


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


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'nivel_interesse')
    search_fields = ('nome',)
    list_filter = ('categoria', 'nivel_interesse')
    filter_horizontal = ('competencias',)


@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autores', 'rating')
    search_fields = ('titulo', 'autores', 'orientadores', 'palavras_chave', 'areas')
    list_filter = ('rating', 'licenciaturas')
    filter_horizontal = ('licenciaturas',)


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'unidade_curricular', 'data_realizacao', 'nota_obtida')
    search_fields = ('titulo', 'descricao')
    list_filter = ('unidade_curricular', 'data_realizacao')
    filter_horizontal = ('tecnologias',)