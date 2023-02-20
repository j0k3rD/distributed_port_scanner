from .tasks import scan_with_python, scan_with_nmap
from flask import Blueprint, render_template, request, current_app
from .services import *
import requests, json
from .services.functions import *
from celery.result import AsyncResult
from .tasks import *


app = Blueprint('app', __name__, url_prefix='/')


@app.route('/', methods=['GET'])
def index():
    scanners = get_scanneers_list()
    scanners_list = json_load(scanners)
    return render_template('index.html', scanners=scanners_list)


@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        ip = request.form['ip']
        port_range = request.form['port_range']
        scan_type = request.form['scan_method']
        #Creamos un usuario y guardamos el escaneo en la base de datos
        mac = get_user_mac()
        save_user = add_user(mac)
        #Creamos un escaneo y guardamos el escaneo en la base de datos
        scanner_data = {
            'mac': mac, 
            'scanner_type': scan_type,
            'ip': ip,
            'port': port_range,
            'status': 'En proceso..',
            'result': 'None'
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{current_app.config["API_URL"]}/scanners', json=scanner_data, headers=headers)
        #Ejecutamos el escaneo
        if response.ok:
            response = json_load(response)
            scan_id = response.get('id')
            scan = scan_task.delay(scan_id)
            return render_template('index.html', scan_result=scan, scan_type=scan_type, ip=ip, port_range=port_range)
        else:
            return 'Error to save scan'


@app.route('/task/<task_id>')
def get_task_status(task_id):
    task = AsyncResult(task_id)
    response = {
        'status': task.status,
        'result': task.result,
        'traceback': task.traceback
    }
    return json.dumps(response)