from celery import Celery, socket, os
from .services.port_scanning import *

CELERY_BRKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

app = Celery('tasks', broker=CELERY_BRKER_URL, backend=CELERY_RESULT_BACKEND)

@app.task
def scan_ports_python(ip, port):
    ip = input(IPV4_INPUT)
    port = input(PORT_INPUT)
    option = input(PYTHON_OR_NMAP)
    if option == '1':
        scan_with_python(ip, port)
    elif option == '2':
        scan_with_nmap(ip, port)
    else:
        print(INVALID_OPTION)
    
    return {'status': 'Task Completed!'}