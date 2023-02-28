from distributed_scanner.celery import app
from .models import Scan
from .services.port_scanning_ipv4 import *
from .services.port_scanning_ipv6 import *
from celery import current_app


# def get_num_workers():
#     # Ajustar el autoescalamiento de los workers de Celery
#     num_workers = current_app.control.inspect().active()
#     if num_workers and len(num_workers) > 2:
#         return 16
#     else:
#         return 2


@app.task(bind=True)
def scan_task(self, scan_id):
    execution = Scan.objects.get(id=scan_id)
    print(execution)
    scan_type = execution.scanner_type
    ipv_type = execution.ipv_type
    ip = execution.ip
    port = execution.port
    try:
        if ipv_type == 'ipv4': 
            if scan_type == 'python':
                scan_result = scan_with_python_ipv4(ip, port)
            elif scan_type == 'nmap':
                scan_result = scan_with_nmap_ipv4(ip, port)
            if execution.port == '':
                execution.port = '0-65535'
            execution.result = scan_result
            execution.status = Scan.STATUS_SUCCESS
        elif ipv_type == 'ipv6':
            if scan_type == 'python':
                scan_result = scan_with_python_ipv6(ip, port)
            elif scan_type == 'nmap':
                scan_result = scan_with_nmap_ipv6(ip, port)
            if execution.port == '':
                execution.port = '0-65535'
            execution.result = scan_result
            execution.status = Scan.STATUS_SUCCESS
    except Exception as e:
        execution.status = Scan.STATUS_ERROR
        execution.message = str(e)[:110]
    
    execution.save()

    # num_workers = get_num_workers()
    # actualizar el autoescalamiento de los workers de Celery
    # current_app.control.broadcast('autoscale', reply=True, min=4, max=num_workers)