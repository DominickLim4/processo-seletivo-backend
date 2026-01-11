from .celery import app as celery_app

__all__ = ('celery_app',)  # Carrega o celery ao iniciar o django
