from django.urls import path
from . import views

urlpatterns = [
    path('licenciaturas/', views.licenciaturas_view, name="licenciaturas"),
    path('docentes/', views.docentes_view, name="docentes"),
    path('competencias/', views.competencias_view, name="competencias"),
    path('formacoes/', views.formacoes_view, name="formacoes"),
    path('tecnologias/', views.tecnologias_view, name="tecnologias"),
]