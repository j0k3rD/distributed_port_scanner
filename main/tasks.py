from main import Celery
from .services.port_scanning import *
from .services import *
import os
from main.services.functions import *
from main.models import ScannerModel


celery = Celery(__name__)
celery.config_from_object('main.config.Config')

@celery.task(bind=True)
def scan_task(self, scan_id):
    scanner = get_scan_by_id(scan_id)
    response = json_load(scanner)
    try:
        if response.get('scanner_type') == 'python':
            scan_result = scan_with_python(response.get('ip'), response.get('port'))
        elif response.get('scanner_type') == 'nmap':
            scan_result = scan_with_nmap(response.get('ip'), response.get('port'))
        response.get('status') == 'Completado'
        response.get('result') == scan_result
    except Exception as e:
        response.get('status') == 'Error'
        response.get('result') == str(e)[:110]
    save_scan = modify_scan(scan_id, response.get('scanner_type'), response.get('id'), response.get('port'), response.get('result'), response.get('status'),)
    return response.get('result')
    

@celery.task(bind=True)
def scan_with_nmap(ip, port_range):
    scan = os.system('nmap -p {} {}'.format(port_range, ip))
    return scan    