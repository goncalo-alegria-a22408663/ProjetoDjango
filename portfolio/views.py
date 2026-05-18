from django.shortcuts import render, redirect
from .forms import ProjetoForm, TecnologiaForm, CompetenciaForm, FormacaoForm
from .models import Licenciatura, Docente, Competencia, Formacao, Tecnologia, UnidadeCurricular, TFC, Projeto, MakingOf, Tipo
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test


def is_gestor_portfolio(user):
    return user.is_authenticated and user.groups.filter(name='gestor-portfolio').exists()


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


@user_passes_test(is_gestor_portfolio)
def novo_projeto_view(request):
    form = ProjetoForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('projetos')

    context = {'form': form}
    return render(request, 'portfolio/novo_projeto.html', context)


@user_passes_test(is_gestor_portfolio)
def edita_projeto_view(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)

    if request.POST:
        form = ProjetoForm(request.POST or None, request.FILES, instance=projeto)
        if form.is_valid():
            form.save()
            return redirect('projetos')
    else:
        form = ProjetoForm(instance=projeto)

    context = {'form': form, 'projeto': projeto}
    return render(request, 'portfolio/edita_projeto.html', context)


@user_passes_test(is_gestor_portfolio)
def apaga_projeto_view(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    projeto.delete()
    return redirect('projetos')


@user_passes_test(is_gestor_portfolio)
def nova_tecnologia_view(request):
    form = TecnologiaForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('tecnologias')

    context = {'form': form}
    return render(request, 'portfolio/nova_tecnologia.html', context)


@user_passes_test(is_gestor_portfolio)
def edita_tecnologia_view(request, tecnologia_id):
    tecnologia = Tecnologia.objects.get(id=tecnologia_id)

    if request.POST:
        form = TecnologiaForm(request.POST or None, request.FILES, instance=tecnologia)
        if form.is_valid():
            form.save()
            return redirect('tecnologias')
    else:
        form = TecnologiaForm(instance=tecnologia)

    context = {'form': form, 'tecnologia': tecnologia}
    return render(request, 'portfolio/edita_tecnologia.html', context)


@user_passes_test(is_gestor_portfolio)
def apaga_tecnologia_view(request, tecnologia_id):
    tecnologia = Tecnologia.objects.get(id=tecnologia_id)
    tecnologia.delete()
    return redirect('tecnologias')


@user_passes_test(is_gestor_portfolio)
def nova_competencia_view(request):
    form = CompetenciaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('competencias')

    context = {'form': form}
    return render(request, 'portfolio/nova_competencia.html', context)


@user_passes_test(is_gestor_portfolio)
def edita_competencia_view(request, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id)

    if request.POST:
        form = CompetenciaForm(request.POST or None, instance=competencia)
        if form.is_valid():
            form.save()
            return redirect('competencias')
    else:
        form = CompetenciaForm(instance=competencia)

    context = {'form': form, 'competencia': competencia}
    return render(request, 'portfolio/edita_competencia.html', context)


@user_passes_test(is_gestor_portfolio)
def apaga_competencia_view(request, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id)
    competencia.delete()
    return redirect('competencias')


@user_passes_test(is_gestor_portfolio)
def nova_formacao_view(request):
    form = FormacaoForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('formacoes')

    context = {'form': form}
    return render(request, 'portfolio/nova_formacao.html', context)


@user_passes_test(is_gestor_portfolio)
def edita_formacao_view(request, formacao_id):
    formacao = Formacao.objects.get(id=formacao_id)

    if request.POST:
        form = FormacaoForm(request.POST or None, request.FILES, instance=formacao)
        if form.is_valid():
            form.save()
            return redirect('formacoes')
    else:
        form = FormacaoForm(instance=formacao)

    context = {'form': form, 'formacao': formacao}
    return render(request, 'portfolio/edita_formacao.html', context)


@user_passes_test(is_gestor_portfolio)
def apaga_formacao_view(request, formacao_id):
    formacao = Formacao.objects.get(id=formacao_id)
    formacao.delete()
    return redirect('formacoes')


def sobre_view(request):
    tipos = Tipo.objects.prefetch_related('tecnologias').all()
    makingof_path = os.path.join(settings.BASE_DIR, 'MakingOf.md')

    try:
        with open(makingof_path, 'r', encoding='utf-8') as f:
            makingof_content = f.read()
    except FileNotFoundError:
        makingof_content = "Ficheiro MakingOf.md não encontrado."

    return render(request, 'portfolio/sobre.html', {
        'tipos': tipos,
        'makingof_content': makingof_content,
    })