from flask import Flask, render_template, request, redirect, url_for, flash
from . import app
from services.port_scanning import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        ip = request.form['ip']
        port = request.form['port']
        option = request.form['option']
        if option == '1':
            scan_with_python.delay(ip, port)
        elif option == '2':
            scan_with_nmap.delay(ip, port)
        else:
            return 'Invalid option'
        return redirect(url_for('index'))
    return render_template('scan.html')

@app.route('/scan/<ip>/<port>/<option>')
def scan_with_params(ip, port, option):
    if option == '1':
        scan_with_python.delay(ip, port)
    elif option == '2':
        scan_with_nmap.delay(ip, port)
    else:
        return 'Invalid option'
    return redirect(url_for('index'))