#Librerias
import re
import socket
import os
import subprocess
import sys
from port_scanning_ipv4 import *

#Constantes
IPV6_INPUT = 'Enter the IPv6 or IPv6 range to scan: '
IPV6_REGEX = r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
IPV6_RANGE_REGEX = r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))-(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
INVALID_IPV6 = 'The IPv6 entered is not valid.'
INVALID_IPV6S = 'Invalid IPV6 or IPV6 range.'


def is_ipv6(ip):
    return re.match(IPV6_REGEX, ip)

def is_ipv6_range(ip_range):
    return re.match(IPV6_RANGE_REGEX, ip_range)

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
        for port in port_range:

            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(OPEN_PORT.format(port=port))
            sock.close()

    elif is_ipv6_range(ip):
        ip_range = ip.split('-')
        if len(ip_range) == 1:
            ip_range.append(ip_range[0])
        ip_range = range(int(ip_range[0], 16), int(ip_range[1], 16) + 1)
        ip_range = [hex(ip)[2:] for ip in ip_range]
        for ip in ip_range:
            for port in port_range:
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    print(OPEN_PORT.format(port=port))
                sock.close()
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
        
    
def main():
    ip = input(IPV6_INPUT)
    port_range = input(PORT_INPUT)
    option = input(PYTHON_OR_NMAP)
    if option == '1':
        print(scan_with_python_ipv6(ip, port_range))
    elif option == '2':
        print(scan_with_nmap_ipv6(ip, port_range))
    else:
        print(INVALID_OPTION)

if __name__ == '__main__':
    main()