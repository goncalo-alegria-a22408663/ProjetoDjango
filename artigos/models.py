from django.db import models
from django.contrib.auth.models import User


class Artigo(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    fotografia = models.ImageField(upload_to='artigos/', blank=True)
    link_externo = models.URLField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artigos')

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.artigo.titulo}"


class Like(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='likes')
    # Pode ser anónimo (qualquer pessoa pode gostar)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('artigo', 'user'),  # um like por user autenticado
        ]