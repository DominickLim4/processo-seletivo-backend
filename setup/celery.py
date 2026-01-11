import os
from celery import Celery


# Define as confgurações padrões do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

app = Celery('setup')

# Lê as config do settings que tenham CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre tarefas dentro dos apps instalados
app.autodiscover_tasks()
