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


class Docente(models.Model):
    HABILITACAO_CHOICES = [
        ('ALU_MES', 'Aluno de Mestrado'),
        ('MES', 'Mestrado'),
        ('ALU_DOUT', 'Aluno de Doutoramento'),
        ('DOUT', 'Doutoramento'),
        ('AGR', 'Agregação'),
    ]

    REGIME_CHOICES = [
        ('TI', 'Tempo Integral'),
        ('TP', 'Tempo Parcial'),
    ]

    nome = models.CharField(max_length=200)
    link_pagina_pessoal = models.URLField(blank=True)
    foto = models.ImageField(upload_to='docentes/', blank=True)
    habilitacao = models.CharField(max_length=10, choices=HABILITACAO_CHOICES)
    regime_contrato = models.CharField(max_length=5, choices=REGIME_CHOICES)

    def __str__(self):
        return self.nome


class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20)
    ano = models.IntegerField()
    semestre = models.IntegerField()
    ects = models.IntegerField()
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='ucs/', blank=True)
    link_pagina = models.URLField(blank=True)

    licenciaturas = models.ManyToManyField(Licenciatura, related_name='unidades_curriculares')
    docentes = models.ManyToManyField(Docente, related_name='unidades_curriculares', blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Competencia(models.Model):
    TIPO_CHOICES = [
        ('TEC', 'Técnica'),
        ('SOFT', 'Soft Skill'),
        ('LING', 'Linguística'),
    ]

    NIVEL_CHOICES = [
        ('BAS', 'Básico'),
        ('INT', 'Intermédio'),
        ('AVA', 'Avançado'),
    ]

    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES)
    nivel = models.CharField(max_length=5, choices=NIVEL_CHOICES)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome