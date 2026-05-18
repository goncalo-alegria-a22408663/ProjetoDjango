from django.urls import path
from . import views

urlpatterns = [
    path('licenciaturas/', views.licenciaturas_view, name="licenciaturas"),
    path('docentes/', views.docentes_view, name="docentes"),
    path('competencias/', views.competencias_view, name="competencias"),
    path('formacoes/', views.formacoes_view, name="formacoes"),
    path('tecnologias/', views.tecnologias_view, name="tecnologias"),
    path('ucs/', views.ucs_view, name="ucs"),
    path('tfcs/', views.tfcs_view, name="tfcs"),
    path('projetos/', views.projetos_view, name="projetos"),
    path('makingofs/', views.makingofs_view, name="makingofs"),
    path('projeto/novo/', views.novo_projeto_view, name="novo_projeto"),
    path('projeto/<int:projeto_id>/edita', views.edita_projeto_view, name="edita_projeto"),
    path('projeto/<int:projeto_id>/apaga', views.apaga_projeto_view, name="apaga_projeto"),
    path('tecnologia/nova/', views.nova_tecnologia_view, name="nova_tecnologia"),
    path('tecnologia/<int:tecnologia_id>/edita', views.edita_tecnologia_view, name="edita_tecnologia"),
    path('tecnologia/<int:tecnologia_id>/apaga', views.apaga_tecnologia_view, name="apaga_tecnologia"),
    path('competencia/nova/', views.nova_competencia_view, name="nova_competencia"),
    path('competencia/<int:competencia_id>/edita', views.edita_competencia_view, name="edita_competencia"),
    path('competencia/<int:competencia_id>/apaga', views.apaga_competencia_view, name="apaga_competencia"),
    path('formacao/nova/', views.nova_formacao_view, name="nova_formacao"),
    path('formacao/<int:formacao_id>/edita', views.edita_formacao_view, name="edita_formacao"),
    path('formacao/<int:formacao_id>/apaga', views.apaga_formacao_view, name="apaga_formacao"),
]