from distributed_scanner.celery import app
from .models import Scan
from .services.port_scanning import *


@app.task(bind=True)
def scan_task(self, scan_id):
    execution = Scan.objects.get(id=scan_id)
    print(execution)
    scan_type = execution.scanner_type
    ip = execution.ip
    port = execution.port
    try:
        if scan_type == 'python':
            scan_result = scan_with_python(ip, port)
        elif scan_type == 'nmap':
            scan_result = scan_with_nmap(ip, port)
        execution.result = scan_result
        execution.status = Scan.STATUS_SUCCESS
    except Exception as e:
        execution.status = Scan.STATUS_ERROR
        execution.message = str(e)[:110]
    
    execution.save()