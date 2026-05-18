from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib.auth import login
from .models import Artigo, Comentario, Like
from .forms import ArtigoForm, ComentarioForm


def is_autor(user):
    return user.is_authenticated and user.groups.filter(name='autores').exists()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def artigos_view(request):
    artigos = Artigo.objects.select_related('autor').prefetch_related('comentarios', 'likes').order_by('-data_criacao')
    return render(request, 'artigos/artigos.html', {'artigos': artigos})


def artigo_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    form_comentario = ComentarioForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form_comentario = ComentarioForm(request.POST)
        if form_comentario.is_valid():
            comentario = form_comentario.save(commit=False)
            comentario.artigo = artigo
            comentario.autor = request.user
            comentario.save()
            return redirect('artigo', artigo_id=artigo.id)

    return render(request, 'artigos/artigo.html', {
        'artigo': artigo,
        'form_comentario': form_comentario,
    })


@user_passes_test(is_autor)
def novo_artigo_view(request):
    form = ArtigoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        artigo = form.save(commit=False)
        artigo.autor = request.user
        artigo.save()
        return redirect('artigos')

    return render(request, 'artigos/novo_artigo.html', {'form': form})


@user_passes_test(is_autor)
def edita_artigo_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)

    # Cada autor só pode editar os seus próprios artigos
    if artigo.autor != request.user:
        return redirect('artigos')

    if request.POST:
        form = ArtigoForm(request.POST or None, request.FILES or None, instance=artigo)
        if form.is_valid():
            form.save()
            return redirect('artigo', artigo_id=artigo.id)
    else:
        form = ArtigoForm(instance=artigo)

    return render(request, 'artigos/edita_artigo.html', {'form': form, 'artigo': artigo})


@user_passes_test(is_autor)
def apaga_artigo_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    if artigo.autor == request.user:
        artigo.delete()
    return redirect('artigos')


def like_artigo_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)

    if request.user.is_authenticated:
        Like.objects.get_or_create(artigo=artigo, user=request.user)
    else:
        ip = get_client_ip(request)
        # Para anónimos, não há unique_together por IP — limitamos manualmente
        if not Like.objects.filter(artigo=artigo, ip=ip, user=None).exists():
            Like.objects.create(artigo=artigo, ip=ip)

    return redirect('artigo', artigo_id=artigo.id)


def registo_autor_view(request):
    """Registo que adiciona automaticamente ao grupo autores."""
    from accounts.forms import RegistoForm

    if request.method == "POST":
        form = RegistoForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo_autores = Group.objects.get(name='autores')
            user.groups.add(grupo_autores)
            login(request, user)
            return redirect('artigos')
    else:
        from accounts.forms import RegistoForm
        form = RegistoForm()

    return render(request, 'artigos/registo_autor.html', {'form': form})