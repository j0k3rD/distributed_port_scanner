from .tasks import scan_with_python, scan_with_nmap
from flask import Blueprint, render_template, request, redirect, url_for
from .services import *
from celery.result import AsyncResult

app = Blueprint('app', __name__, url_prefix='/')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    scan_result = None
    ip = None
    port_range = None
    scan_type = None
    if request.method == 'POST':
        ip = request.form['ip']
        port_range = request.form['port_range']
        scan_type = request.form['scan_method']
        if scan_type == 'python':
            scan_result = scan_with_python.delay(ip, port_range)
        elif scan_type == 'nmap':
            scan_result = scan_with_nmap.delay(ip, port_range)

    if scan_result and scan_result.ready():
        # Save the result to the database
        response = scan_result.get()
    else:
        response = scan_result.get()

    return render_template('scan.html', scan_result=response, scan_type=scan_type, ip=ip, port_range=port_range)