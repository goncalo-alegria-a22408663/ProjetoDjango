from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('registo/', views.registo_view, name="registo"),
    path('login-magic-link/', views.login_magic_link_view, name="login_magic_link"),
    path('autentica/', views.autentica_view, name="autentica"),
]