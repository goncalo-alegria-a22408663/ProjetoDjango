from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .forms import RegistoForm


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