import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distributed_scanner.settings')

app = Celery('distributed_scanner')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Configuración para autoscaling
# @app.task
# def get_queue_size():
#     return app.control.inspect().active_queues()

# @app.task
# def get_queue_length():
#     return sum([len(app.control.inspect().active()[worker]) for worker in app.control.inspect().active()])

# @app.task
# def get_queue_depth():
#     return sum([len(app.control.inspect().active()[worker]) for worker in app.control.inspect().scheduled()])

# @app.task
# def should_scale_down():
#     return get_queue_depth() == 0

# @app.task
# def should_scale_up():
#     return get_queue_length() > 2

# @app.task
# def get_num_workers():
#     # si son mas de 2 tareas pendientes levantar todos los workers
#     if should_scale_up():
#         return min(16, max(2, int(get_queue_length() / 2)))
#     elif should_scale_down():
#         return max(2, int(get_queue_length() / 2))
#     else:
#         return get_queue_length()

# CELERYBEAT_SCHEDULE = {
#     'scale-workers': {
#         'task': 'distributed_scanner.celery.get_num_workers',
#         'schedule': 10.0, # cada 10 segundos verifica la cantidad de tareas pendientes
#     },
# }

# app.conf.beat_schedule = CELERYBEAT_SCHEDULE