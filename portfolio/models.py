from django.db import models


class Licenciatura(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=10)
    instituicao = models.CharField(max_length=200)
    descricao = models.TextField()
    duracao_anos = models.IntegerField()
    total_ects = models.IntegerField()
    link_oficial = models.URLField(blank=True)
    imagem = models.ImageField(upload_to='licenciaturas/', blank=True)

    def __str__(self):
        return self.sigla