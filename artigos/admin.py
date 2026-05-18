from django.contrib import admin
from .models import Artigo, Comentario, Like


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_criacao')
    search_fields = ('titulo', 'texto')
    list_filter = ('autor', 'data_criacao')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'autor', 'data_criacao')
    list_filter = ('artigo', 'data_criacao')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'user', 'ip', 'data_criacao')
    list_filter = ('artigo',)