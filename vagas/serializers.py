from rest_framework import serializers
from .models import Vaga


# Objeto Python -> JSON (Enviar para o React)
# JSON -> Objeto Python (Salvar no Banco)
class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaga
        fields = '__all__'  # Serializa todos os campos do modelo
