from main import Celery
from .services.port_scanning import *
from .services import *
import os
from subprocess import Popen, PIPE

celery = Celery(__name__)
celery.config_from_object('main.config.Config')

@celery.task
def scan_with_python(ip, port_range):
    ips_list = []
    if is_ipv4(ip):
        open_ports = scan_ipv4(ip, port_range)
        return OPEN_PORTS.format(ip=ip, open_ports=open_ports)
    elif is_ipv4_range(ip):
        open_ports = scan_ipv4_range(ip, port_range)
        for ip, ports in open_ports.items():
            ips_list.append(OPEN_PORTS.format(ip=ip, open_ports=ports))
        return ips_list
    else:
        return INVALID_IPV4


@celery.task
def scan_with_nmap(ip, port_range):
    scan = os.system('nmap -p {} {}'.format(port_range, ip))
    return scan    