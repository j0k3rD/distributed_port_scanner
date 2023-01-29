from celery import Celery, os
from .services.port_scanning import *
from .services.save_scan import *

@celery.task
def scan_with_python(ip, port_range):
    open_ports = scan_ipv4(ip, port_range)
    save_scan(ip, port_range, open_ports)