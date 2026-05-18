from django import forms
from .models import Projeto, Tecnologia, Competencia, Formacao


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'
        widgets = {
            'data_realizacao': forms.DateInput(attrs={'type': 'date'}),
        }