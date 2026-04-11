import json
import os
from django.core.management.base import BaseCommand
from portfolio.models import Licenciatura, UnidadeCurricular


class Command(BaseCommand):
    help = 'Carrega Curso e UCs a partir dos JSONs em data/lusofona/'

    def handle(self, *args, **options):
        data_dir = os.path.join('data', 'lusofona')
        course_code = 260
        language = 'PT'

        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR(f'Pasta não encontrada: {data_dir}'))
            return

        curso_path = os.path.join(data_dir, f'ULHT{course_code}-{language}.json')
        if not os.path.exists(curso_path):
            self.stdout.write(self.style.ERROR(f'Ficheiro do curso não encontrado: {curso_path}'))
            return

        with open(curso_path, 'r', encoding='utf-8') as f:
            curso_data = json.load(f)

        nome_curso = curso_data.get('courseName', 'Licenciatura em Engenharia Informática')

        licenciatura, created = Licenciatura.objects.get_or_create(
            sigla='LEI',
            defaults={
                'nome': nome_curso,
                'instituicao': 'Universidade Lusófona',
                'descricao': curso_data.get('courseDescription', '') or '',
                'duracao_anos': 3,
                'total_ects': 180,
                'link_oficial': 'https://www.ulusofona.pt/lisboa/licenciaturas/engenharia-informatica',
            }
        )
        if not created:
            licenciatura.nome = nome_curso
            licenciatura.save()

        self.stdout.write(self.style.SUCCESS(f'Licenciatura: {licenciatura.sigla} - {licenciatura.nome}'))

        ucs_criadas = 0
        ucs_existentes = 0

        for uc in curso_data.get('courseFlatPlan', []):
            codigo = uc.get('curricularIUnitReadableCode', '').strip()
            nome = uc.get('curricularIUnitName', '').strip()

            if not codigo:
                continue

            uc_path = os.path.join(data_dir, f'{codigo}-{language}.json')
            uc_detail = {}
            if os.path.exists(uc_path):
                with open(uc_path, 'r', encoding='utf-8') as f:
                    uc_detail = json.load(f)

            ano = uc.get('curricularYear', 1) or 1
            semestre_code = str(uc.get('semesterCode', 'S'))
            if semestre_code == '1':
                semestre = 1
            elif semestre_code == '2':
                semestre = 2
            else:
                semestre = 1

            ects = int(uc.get('ects', 6) or 6)
            descricao = uc_detail.get('objectives', '') or uc_detail.get('program', '') or ''

            uc_obj, uc_created = UnidadeCurricular.objects.get_or_create(
                codigo=codigo,
                defaults={
                    'nome': nome,
                    'ano': ano,
                    'semestre': semestre,
                    'ects': ects,
                    'descricao': descricao,
                }
            )
            uc_obj.licenciaturas.add(licenciatura)

            if uc_created:
                ucs_criadas += 1
            else:
                ucs_existentes += 1

        self.stdout.write(self.style.SUCCESS(
            f'Carregamento concluído: {ucs_criadas} UCs criadas, {ucs_existentes} já existiam'
        ))