from celery import Celery
from .services.port_scanning import *
from .services.save_scan import *

celery = Celery(__name__)
celery.config_from_object('main.config.Config')

@celery.task
def scan_with_python(ip, port_range):
    if is_ipv4(ip):
        open_ports = scan_ipv4(ip, port_range)
    elif is_ipv4_range(ip):
        open_ports = scan_ipv4_range(ip, port_range)
    else:
        return 'Invalid IP'
    # save_scan(ip, port_range, open_ports)
    return open_ports

@celery.task
def scan_with_nmap(ip, port_range):
    os.system('nmap -p {} {}'.format(port_range, ip))
    return 'Scan finished'