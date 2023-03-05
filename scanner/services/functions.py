import json
from subprocess import Popen, PIPE
        
def get_user_mac():
    operation = Popen(['cat', '/sys/class/net/eth0/address'], stdout=PIPE, stderr=PIPE)
    output, error = operation.communicate()
    if operation.returncode != 0:
        operation = Popen(['cat', '/sys/class/net/wlp2s0/address'], stdout=PIPE, stderr=PIPE)
    return operation.stdout.read().decode('utf-8').strip()

def get_hostname():
    hostname = Popen(['hostname'], stdout=PIPE).communicate()[0]
    return hostname.decode('utf-8').strip()

def json_load(response):
    return json.loads(response.text)