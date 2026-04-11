import json
import os
from django.core.management.base import BaseCommand
from portfolio.models import TFC, Licenciatura


class Command(BaseCommand):
    help = 'Carrega TFCs a partir do ficheiro data/tfcs_2025.json'

    def handle(self, *args, **options):
        json_path = os.path.join('data', 'tfcs_2025.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'Ficheiro não encontrado: {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            tfcs_data = json.load(f)

        criados = 0
        ignorados = 0

        for tfc_data in tfcs_data:
            licenciaturas_str = tfc_data.get('licenciaturas', '').strip()

            if 'Licenciatura' not in licenciaturas_str:
                ignorados += 1
                continue

            tfc, created = TFC.objects.get_or_create(
                titulo=tfc_data.get('titulo', '').strip(),
                defaults={
                    'sumario': tfc_data.get('sumario', '').strip(),
                    'autores': tfc_data.get('autores', '').strip(),
                    'orientadores': tfc_data.get('orientadores', '').strip(),
                    'imagem': tfc_data.get('imagem', '').strip(),
                    'link_pdf': tfc_data.get('link_pdf', '').strip(),
                    'palavras_chave': tfc_data.get('palavras_chave', '').strip(),
                    'areas': tfc_data.get('areas', '').strip(),
                    'tecnologias_usadas': tfc_data.get('tecnologias_usadas', '').strip(),
                    'rating': tfc_data.get('rating', 3) or 3,
                }
            )

            licenciaturas_nomes = [l.strip() for l in licenciaturas_str.split('.') if l.strip()]
            for lic_nome in licenciaturas_nomes:
                licenciatura, _ = Licenciatura.objects.get_or_create(
                    nome=lic_nome,
                    defaults={
                        'sigla': lic_nome[:10],
                        'instituicao': 'Universidade Lusófona',
                        'descricao': '',
                        'duracao_anos': 3,
                        'total_ects': 180,
                    }
                )
                tfc.licenciaturas.add(licenciatura)

            if created:
                criados += 1

        self.stdout.write(self.style.SUCCESS(
            f'Carregamento concluído: {criados} TFCs criados, {ignorados} ignorados'
        ))