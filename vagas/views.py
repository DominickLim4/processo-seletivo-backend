# vagas/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from celery.result import AsyncResult  # Necessário para checar status
from .models import Vaga
from .serializers import VagaSerializer
from .tasks import exportar_relatorio_vagas


class VagaViewSet(viewsets.ModelViewSet):
    # ViewSet que Herda ModelViewSet (LIST,CREATE,RETRIEVE...)
    queryset = Vaga.objects.all().order_by('-criado_em')
    serializer_class = VagaSerializer

    # 1. Gatilho da Exportação
    # Endpoint: POST /api/vagas/exportar_relatorio/
    @action(detail=False, methods=['post'])
    def exportar_relatorio(self, request):
        # Pega o formato enviado pelo front (padrão é excel)
        formato = request.data.get('formato', 'excel')

        # Inicia a task passando o formato
        # Usa .delay() para passar para o Celery
        # Libera a requisição e usuário não fica travado
        task = exportar_relatorio_vagas.delay(formato=formato)

        return Response({
            "task_id": task.id,
            "mensagem": f"Exportação de {formato} iniciada."
        })

    # 2. Consulta o Status (Polling)
    # Endpoint: GET /api/vagas/status_tarefa/{task_id}/
    @action(detail=False, methods=['get'], url_path='status_tarefa/(?P<task_id>[^/.]+)') # noqa
    def status_tarefa(self, request, task_id=None):
        # Consulta o Redis para saber o estado dessa tarefa específica
        task_result = AsyncResult(task_id)

        if task_result.ready():
            # Se acabou, retorna o resultado da task (a URL do arquivo)
            result_data = task_result.result
            return Response({
                "status": "CONCLUIDO",
                "url": result_data.get('url') if isinstance(result_data, dict) else None # noqa
            })
        else:
            return Response({"status": "PROCESSANDO"})
