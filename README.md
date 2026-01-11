# 📘 Manual Técnico: Spassu Vagas (Backend)

> **Projeto de Avaliação Técnica**
> Este documento detalha a arquitetura, decisões de engenharia e instruções de execução da API

---

## 1. Arquitetura e Decisões Técnicas

O backend foi construído seguindo o padrão **API REST** com **Processamento Assíncrono**.

### 1.1 Stack Tecnológica
* **Framework:** Django + Django REST Framework
* **Mensageria:** Redis
* **Task Queue:** Celery
* **Geradores de Arquivos:** Pandas (Excel) e ReportLab (PDF)
* **Qualidade:** Flake8 (Linter) e APITestCase (Testes)

---

## 2. Guia de Instalação e Execução

### Pré-requisitos
1.  **Python 3.10+**
2.  **Redis Server** rodando (Porta 6379)

### Passo a Passo

1.  **Configurar Ambiente:**
    ```bash
    cd nome-da-pasta
    python -m venv venv
    
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    
    pip install -r requirements.txt
    ```

2.  **Banco de Dados:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3.  **Rodar a Aplicação (Necessário 2 Terminais):**

    * **Terminal 1 (Django):**
        ```bash
        python manage.py runserver
        ```

    * **Terminal 2 (Celery Worker):**
        ```bash
        # Linux/Mac:
        celery -A setup worker -l info
        
        # Windows:
        celery -A setup worker -l info --pool=solo
        ```

---

## 3. Testes e Qualidade

Execute os comandos abaixo para garantir a integridade do código:

* **Testes de Integração:** Verifica endpoints e regras de negócio
    ```bash
    python manage.py test
    ```

* **Linter (PEP8):** Verifica estilo de código
    ```bash
    flake8
    ```

---

## 📡 4. Mapa da API

* `GET /api/vagas/`: Listagem
* `POST /api/vagas/`: Cadastro
* `POST /api/vagas/exportar_relatorio/`: Inicia tarefa assíncrona (Retorna `task_id`)
* `GET /api/vagas/status_tarefa/{id}/`: Consulta status do processamento (Polling)