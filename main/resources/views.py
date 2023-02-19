from ..tasks import scan_with_python, scan_with_nmap
from flask import Blueprint, render_template, request, current_app
from ..services import *
import requests, json


app = Blueprint('app', __name__, url_prefix='/')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        ip = request.form['ip']
        port_range = request.form['port_range']
        scan_type = request.form['scan_method']
        if scan_type == 'python':
            scan_result = scan_with_python.delay(ip, port_range)
        elif scan_type == 'nmap':
            scan_result = scan_with_nmap.delay(ip, port_range)
        
        data = {
            'scan_type': scan_type,
            'ip': ip,
            'port': port_range,
            'scan_result': scan_result
        }

        headers = {'Content-Type': 'application/json'}

        response = requests.post(f'{current_app.config["API_URL"]}/scanners', json=data, headers=headers)
        