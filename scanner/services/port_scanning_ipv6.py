#Librerias
import re
import socket
from subprocess import getoutput, Popen, PIPE
from .port_scanning_ipv4 import *
from .services_constants import *


def is_ipv6(ip):
    return re.match(IPV6_REGEX, ip)

def is_ipv6_range(ip_range):
    return re.match(IPV6_RANGE_REGEX, ip_range)

def scan_ipv6(ip, port_range):
    open_ports = []
    for port in port_range:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(OPEN_PORT.format(port=port))
        sock.close()
    result =  ', '.join(['{} {}:{}'.format((OPEN_PORTS), ip, port) for (ip, port) in open_ports])

    if result == '':
        return 'No open ports in {ip}'.format(ip=ip, port=port)
    else:
        return result

def scan_with_python_ipv6(ip, port_range):
    if is_ipv6(ip):
        if port_range == '':
            port_range = '0-65535'
        if is_port(port_range):
            port_range = '{port_range}'.format(port_range=port_range)
        elif is_port_range(port_range):
            port_range = '{port_range}'.format(port_range=port_range)
        else:
            return INVALID_PORT_RANGE
        port_range = port_range.split('-')
        if len(port_range) == 1:
            port_range.append(port_range[0])
        port_range = range(int(port_range[0]), int(port_range[1]) + 1)
        scan = scan_ipv6(ip, port_range)
        return scan
    # A testear
    elif is_ipv6_range(ip):
        ip_range = ip.split('-')
        if len(ip_range) == 1:
            ip_range.append(ip_range[0])
        ip_range = range(int(ip_range[0], 16), int(ip_range[1], 16) + 1)
        ip_range = [hex(ip)[2:] for ip in ip_range]
        scan = scan_ipv6(ip, port_range)
        return scan
    else:   
        return INVALID_IPV6S
    
def scan_with_nmap_ipv6(ip_range, port_range):
    if not is_nmap_installed():
        return NMAP_NOT_INSTALLED
    
    if not is_ipv6(ip_range):
        return INVALID_IPV6

    print(port_range)
    if port_range == '':
        port_range = '0-65535'
        
    if '-' in port_range:
        if not is_port_range(port_range):
            return INVALID_PORT_RANGE
    else:
        if not is_port(port_range):
            return INVALID_PORT

    if '-' not in port_range:
        port_range = f"{port_range}-{port_range}"

    if port_range == '0-65535':
        command = ['nmap', '-6', ip_range]
    else:
        command = ['nmap', '-6', '-p', port_range, ip_range]
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        return stderr.decode('utf-8').strip()

    results = stdout.decode('utf-8').strip()
    ips_with_open_ports = []
    for line in results.splitlines():
        if line.startswith('Nmap scan report for '):
            ip = line.split()[-1]
            has_open_ports = False
        elif 'open' in line:
            port = line.split()[0]
            if not has_open_ports:
                has_open_ports = True
                ips_with_open_ports.append(f'{ip}:{port}')
            else:
                ips_with_open_ports[-1] += f', {port}'
    if not ips_with_open_ports:
        return 'No open ports found.'
    else:
        return '\n'.join(ips_with_open_ports)