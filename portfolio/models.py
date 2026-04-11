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


class Tecnologia(models.Model):
    CATEGORIA_CHOICES = [
        ('LING', 'Linguagem'),
        ('FRAME', 'Framework'),
        ('FERR', 'Ferramenta'),
        ('BD', 'Base de Dados'),
    ]

    NIVEL_INTERESSE_CHOICES = [
        (1, '1 - Muito Baixo'),
        (2, '2 - Baixo'),
        (3, '3 - Médio'),
        (4, '4 - Alto'),
        (5, '5 - Muito Alto'),
    ]

    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES)
    descricao = models.TextField()
    logo = models.ImageField(upload_to='tecnologias/', blank=True)
    link_oficial = models.URLField(blank=True)
    nivel_interesse = models.IntegerField(choices=NIVEL_INTERESSE_CHOICES, default=3)
    aspetos_relevantes = models.TextField(blank=True)

    competencias = models.ManyToManyField(Competencia, related_name='tecnologias', blank=True)

    def __str__(self):
        return self.nome


class TFC(models.Model):
    RATING_CHOICES = [
        (1, '1 - Muito Baixo'),
        (2, '2 - Baixo'),
        (3, '3 - Médio'),
        (4, '4 - Alto'),
        (5, '5 - Muito Alto'),
    ]

    titulo = models.CharField(max_length=300)
    sumario = models.TextField()
    autores = models.CharField(max_length=500, blank=True)
    orientadores = models.CharField(max_length=500, blank=True)
    imagem = models.URLField(blank=True)
    link_pdf = models.URLField(blank=True)
    palavras_chave = models.CharField(max_length=500, blank=True)
    areas = models.CharField(max_length=500, blank=True)
    tecnologias_usadas = models.CharField(max_length=500, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=3)

    licenciaturas = models.ManyToManyField(Licenciatura, related_name='tfcs', blank=True)

    def __str__(self):
        return self.titulo


class Projeto(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    conceitos_aplicados = models.TextField(blank=True)
    data_realizacao = models.DateField()
    imagem = models.ImageField(upload_to='projetos/', blank=True)
    link_video_demo = models.URLField(blank=True)
    link_github = models.URLField(blank=True)
    nota_obtida = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    unidade_curricular = models.ForeignKey(
        UnidadeCurricular,
        on_delete=models.CASCADE,
        related_name='projetos'
    )
    tecnologias = models.ManyToManyField(Tecnologia, related_name='projetos', blank=True)

    def __str__(self):
        return self.titulo


class Formacao(models.Model):
    nome = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    descricao = models.TextField(blank=True)
    certificado = models.FileField(upload_to='formacoes/', blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.nome


class MakingOf(models.Model):
    titulo = models.CharField(max_length=200)
    data = models.DateField()
    descricao_processo = models.TextField()
    decisoes_tomadas = models.TextField(blank=True)
    erros_e_correcoes = models.TextField(blank=True)
    uso_ia = models.TextField(blank=True)
    foto_caderno = models.ImageField(upload_to='makingof/', blank=True)

    licenciaturas = models.ManyToManyField(Licenciatura, related_name='makingofs', blank=True)
    ucs = models.ManyToManyField(UnidadeCurricular, related_name='makingofs', blank=True)
    docentes = models.ManyToManyField(Docente, related_name='makingofs', blank=True)
    projetos = models.ManyToManyField(Projeto, related_name='makingofs', blank=True)
    tecnologias = models.ManyToManyField(Tecnologia, related_name='makingofs', blank=True)
    tfcs = models.ManyToManyField(TFC, related_name='makingofs', blank=True)
    competencias = models.ManyToManyField(Competencia, related_name='makingofs', blank=True)
    formacoes = models.ManyToManyField(Formacao, related_name='makingofs', blank=True)

    def __str__(self):
        return self.titulo