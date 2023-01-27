from celery import Celery, os
from .services.port_scanning import *
from .services.save_scan import *

@celery.task
def scan_with_python(ip, port_range):
    if is_ipv4(ip):
        open_ports = scan_ipv4(ip, port_range)
    elif is_ipv4_range(ip):
        open_ports = scan_ipv4_range(ip, port_range)
    else:
        return 'Invalid IP'
    for port in open_ports:
        save_scan.delay(ip, port)
    return 'Scan finished'