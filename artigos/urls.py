from django.urls import path
from . import views

urlpatterns = [
    path('', views.artigos_view, name="artigos"),
    path('novo/', views.novo_artigo_view, name="novo_artigo"),
    path('<int:artigo_id>/', views.artigo_view, name="artigo"),
    path('<int:artigo_id>/edita/', views.edita_artigo_view, name="edita_artigo"),
    path('<int:artigo_id>/apaga/', views.apaga_artigo_view, name="apaga_artigo"),
    path('<int:artigo_id>/like/', views.like_artigo_view, name="like_artigo"),
    path('registo-autor/', views.registo_autor_view, name="registo_autor"),
]