import os
from celery import Celery

# Establecer la variable de entorno DJANGO_SETTINGS_MODULE para que Celery pueda encontrar el archivo settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distributed_scanner.settings')

# Instanciar la aplicación de Celery
app = Celery('distributed_scanner')
# Configurar Celery utilizando las opciones definidas en settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')