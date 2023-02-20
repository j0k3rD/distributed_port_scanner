from flask import request, current_app
import requests, json
from subprocess import Popen, PIPE

def add_user(mac):
    user_data = {
        'mac': mac
    }
    headers = {'Content-Type': 'application/json'}
    return requests.post(f'{current_app.config["API_URL"]}/users', json=user_data, headers=headers)
        
def get_user_mac():
    operation = Popen(['cat', '/sys/class/net/eth0/address'], stdout=PIPE, stderr=PIPE)
    output, error = operation.communicate()
    if operation.returncode != 0:
        operation = Popen(['cat', '/sys/class/net/wlp2s0/address'], stdout=PIPE, stderr=PIPE)
    return operation.stdout.read().decode('utf-8').strip()

def add_scan(mac, scanner_type, ip, port, status, result):
    user_data = {
        'mac': mac, 
        'scanner_type': scanner_type,
        'ip': ip,
        'port': port,
        'status': status,
        'result': result
    }
    headers = {'Content-Type': 'application/json'}
    return requests.post(f'{current_app.config["API_URL"]}/scanners', json=user_data, headers=headers)

def modify_scan(scan_id, scanner_type, ip, port, status, result):
    user_data = {
        'scan_id': scan_id,
        'scanner_type': scanner_type,
        'ip': ip,
        'port': port,
        'status': status,
        'result': result
    }
    headers = {'Content-Type': 'application/json'}
    return requests.put(f'{current_app.config["API_URL"]}/scanner/{scan_id}', json=user_data, headers=headers)

def json_load(response):
    return json.loads(response.text)


def get_scan_by_id(scan_id):
    return requests.get(f'{current_app.config["API_URL"]}/scanner/{scan_id}')

def get_scanneers_list():
    return requests.get(f'{current_app.config["API_URL"]}/scanners')

