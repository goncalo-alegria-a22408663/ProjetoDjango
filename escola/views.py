from django.http import HttpResponse
from .models import Curso

def lista_cursos(request):
    cursos = Curso.objects.all()
    texto = "Cursos:\n" + "\n".join(c.nome for c in cursos)
    return HttpResponse(texto, content_type="text/plain")