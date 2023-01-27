from flask import Flask, render_template, request, redirect, url_for, flash
from . import app
from services.port_scanning import *

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip = request.form['ip']
        port = request.form['port']
        option = request.form['option']
        if option == '1':
            open_ports = scan_with_python(ip, port)
        elif option == '2':
            open_ports = scan_with_nmap(ip, port)
        else:
            return 'Invalid option'
        return render_template('index.html', open_ports=open_ports)
    return render_template('index.html')