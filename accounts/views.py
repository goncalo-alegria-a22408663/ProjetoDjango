from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .forms import RegistoForm
import secrets
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Profile
from django.conf import settings

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('projetos')
        else:
            return render(request, 'accounts/login.html', {
                'mensagem': 'Credenciais inválidas'
            })

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('projetos')


def registo_view(request):
    if request.method == "POST":
        form = RegistoForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('projetos')
    else:
        form = RegistoForm()

    return render(request, 'accounts/registo.html', {'form': form})

def envia_email_magic_link(user, email, request):
    link = request.build_absolute_uri(
        f"/autentica/?token={user.profile.token}"
    )
    send_mail(
        subject='Portfólio: Link de autenticação',
        message=f'Olá {user.first_name or user.username},\n\n'
                f'Clica neste link para entrar no portfólio:\n{link}\n\n'
                f'Se não pediste este link, ignora este email.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )


def login_magic_link_view(request):
    email = request.POST.get('email')

    if not email:
        return render(request, 'accounts/login.html', {
            'mensagem': 'Indica o teu email.'
        })

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        user.profile.token = secrets.token_urlsafe(32)
        user.profile.save()
        envia_email_magic_link(user, email, request)
        return render(request, 'accounts/login.html', {
            'mensagem': 'Link enviado! Verifica o teu email.'
        })
    else:
        return render(request, 'accounts/login.html', {
            'mensagem': 'Não existe utilizador com esse email.'
        })


def autentica_view(request):
    token = request.GET.get('token')

    if not token:
        return redirect('login')

    try:
        profile = Profile.objects.get(token=token)
        user = profile.user
        # invalida o token (uso único)
        profile.token = None
        profile.save()
        login(request, user)
        return redirect('projetos')
    except Profile.DoesNotExist:
        return render(request, 'accounts/login.html', {
            'mensagem': 'Link inválido ou já usado.'
        })