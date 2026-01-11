from django.db import models


# Criação da Tabela de Vagas
class Vaga(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)  # DecimalField para armazenar valor preciso
    criado_em = models.DateTimeField(auto_now_add=True)  # Grava data/hora

    def __str__(self):  # Retorna o Titulo da Vaga
        return self.titulo
