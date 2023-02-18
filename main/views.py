from .tasks import scan_with_python, scan_with_nmap
from flask import Blueprint, render_template, request, redirect, url_for
from services.utils import *


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        ip = request.form['ip']
        port_range = request.form['port_range']
        scan_type = request.form['scan_type']
        if scan_type == 'python':
            scan_with_python.delay(ip, port_range)
            #Guarda en la base de datos
            
        elif scan_type == 'nmap':
            scan_with_nmap.delay(ip, port_range)
        return redirect(url_for('app.index'))
    return render_template('scan.html')