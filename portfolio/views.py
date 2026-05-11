from django.shortcuts import render
from .models import Licenciatura, Docente, Competencia, Formacao, Tecnologia, UnidadeCurricular, TFC, Projeto, MakingOf


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

def ucs_view(request):
    ucs = (UnidadeCurricular.objects.prefetch_related('licenciaturas', 'docentes').all())
    return render(request, 'portfolio/ucs.html', {'ucs': ucs})

def tfcs_view(request):
    tfcs = TFC.objects.prefetch_related('licenciaturas').all()
    return render(request, 'portfolio/tfcs.html', {'tfcs': tfcs})

def projetos_view(request):
    projetos = (Projeto.objects.select_related('unidade_curricular').prefetch_related('tecnologias').all())
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})

def makingofs_view(request):
    makingofs = (MakingOf.objects.prefetch_related('licenciaturas', 'ucs', 'docentes', 'projetos','tecnologias', 'tfcs', 'competencias', 'formacoes').all())
    return render(request, 'portfolio/makingofs.html', {'makingofs': makingofs})