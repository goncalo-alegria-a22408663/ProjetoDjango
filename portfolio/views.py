from django.shortcuts import render
from .models import Licenciatura, Docente, Competencia, Formacao, Tecnologia


def licenciaturas_view(request):
    licenciaturas = Licenciatura.objects.all()
    return render(request, 'portfolio/licenciaturas.html', {'licenciaturas': licenciaturas})


def docentes_view(request):
    docentes = Docente.objects.all()
    return render(request, 'portfolio/docentes.html', {'docentes': docentes})


def competencias_view(request):
    competencias = Competencia.objects.all()
    return render(request, 'portfolio/competencias.html', {'competencias': competencias})


def formacoes_view(request):
    formacoes = Formacao.objects.all()
    return render(request, 'portfolio/formacoes.html', {'formacoes': formacoes})

def tecnologias_view(request):
    tecnologias = Tecnologia.objects.prefetch_related('competencias').all()
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})