from rest_framework.test import APITestCase
from rest_framework import status
from .models import Vaga


class VagaAPITestCase(APITestCase):

    def setUp(self):
        #  Cria um cenário inicial.
        self.vaga_exemplo = Vaga.objects.create(
            titulo="Dev Senior",
            descricao="saber muito",
            salario=10000.00
        )
        self.url = '/api/vagas/'

    def test_deve_listar_vagas(self):
        #  Testa se o GET retorna 200 e a lista correta
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Deve ter 1 vaga (criada no setUp)
        self.assertEqual(response.data[0]['titulo'], "Dev Senior")

    def test_deve_criar_vaga(self):

        #  Testa se o POST cria uma vaga nova
        dados = {
            "titulo": "Dev Junior",
            "descricao": "Aprender muito",
            "salario": 3000.00
        }

        response = self.client.post(self.url, dados)

        # Verifica se retornou 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifica se salvou no banco de verdade
        self.assertEqual(Vaga.objects.count(), 2)  # 1 do setUp + 1 de agora

    def test_validacao_salario_invalido(self):

        # Testa se a API barra dados ruins
        dados = {
            "titulo": "Teste Erro",
            "descricao": "Teste",
            "salario": "mil reais"
        }

        response = self.client.post(self.url, dados)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
