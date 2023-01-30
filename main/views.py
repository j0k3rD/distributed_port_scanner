from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from .services.port_scanning import scan_with_python, scan_with_nmap
# from .services import save_scan

app = Blueprint('app', __name__, url_prefix='/')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        ip = request.form['ip']
        port_range = request.form['port_range']
        if request.form['scan_method'] == 'python':
            scan_with_python.delay(ip, port_range)
        elif request.form['scan_method'] == 'nmap':
            scan_with_nmap.delay(ip, port_range)
        else:
            return 'Invalid scan method'
        return redirect(url_for('app.results'))
    return render_template('scan.html')

@app.route('/results')
def results():
    return render_template('scan.html')