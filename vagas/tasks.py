# vagas/tasks.py
from celery import shared_task
from .models import Vaga
import pandas as pd
from reportlab.pdfgen import canvas
import os
from django.conf import settings
from datetime import datetime
import logging  # 1. Import do Logging


# Configura o logger
# Importante pros logs ficarem salvos com níveis
logger = logging.getLogger(__name__)


@shared_task
def exportar_relatorio_vagas(formato='excel'):
    logger.info(f"Iniciando tarefa de exportação. Formato: {formato}")

    # Garante diretório media que exista
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    # Gera um nome único com data e hora para não sobrescrever arquivos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_url = ""

    try:
        if formato == 'excel':
            # --- LÓGICA EXCEL
            vagas = Vaga.objects.all().values()
            df = pd.DataFrame(list(vagas))

            # O Excel não aceita nativamente colunas com fuso horário misturado
            if 'criado_em' in df.columns:
                df['criado_em'] = pd.to_datetime(df['criado_em']).dt.tz_localize(None)

            filename = f"relatorio_vagas_{timestamp}.xlsx"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)

            df.to_excel(filepath, index=False)
            file_url = f"{settings.MEDIA_URL}{filename}"
            logger.info(f"Excel gerado com sucesso: {filepath}")

        elif formato == 'pdf':
            # --- LÓGICA PDF
            filename = f"relatorio_vagas_{timestamp}.pdf"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)

            # Canvas no modelo de plano cartesiano (x, y)
            c = canvas.Canvas(filepath)
            c.drawString(100, 800, f"Relatório de Vagas - Gerado em {timestamp}")

            y = 750
            for vaga in Vaga.objects.all():
                texto = f"{vaga.titulo} - R$ {vaga.salario}"
                c.drawString(100, y, texto)
                y -= 20
                if y < 50:  # Nova página se acabar espaço
                    c.showPage()
                    y = 800
            c.save()
            file_url = f"{settings.MEDIA_URL}{filename}"
            logger.info(f"PDF gerado com sucesso: {filepath}")

        # Retorna o status e a url para o Frontend
        return {'status': 'concluido', 'url': file_url}

    except Exception as e:
        # Para debuggar
        logger.error(f"Erro na exportação: {str(e)}")
        raise e
