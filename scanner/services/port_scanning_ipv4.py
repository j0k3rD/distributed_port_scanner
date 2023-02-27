import socket, re, os
from subprocess import getoutput, Popen, PIPE


# Constants
IPV4_REGEX = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
# REGEX puertos 0-65535
PORT_RANGE_REGEX = r"^(?:[0-9]{1,5}|6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|0)-(?:[0-9]{1,5}|6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|0)$"
PORT_MIN = 0
PORT_MAX = 65535
IPV4_RANGE_REGEX = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)-(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
IPV4_INPUT = 'Enter the IPv4 or IPv4 range to scan: '
PYTHON_OR_NMAP = '''Enter the option to scan:
                        1. Python
                        2. Nmap
'''
PORT_INPUT = 'Enter the port or port range to scan: '
OPEN_PORTS = 'Open ports in:'
SCANNING = 'Scanning...'
OPEN_PORT = 'The port {port} is open.'
INVALID_PORT = 'The port entered is not valid.'
INVALID_IPV4 = 'The IPv4 entered is not valid.'
INVALID_PORT_RANGE = 'The port range entered is not valid.'
INVALID_IPV4_RANGE = 'The IPv4 range entered is not valid.'
INVALID_IPV6_RANGE = 'The IPv6 range entered is not valid.'
INVALID_IPV4S = 'Invalid IPV4 or IPV4 range.'
INVALID_OPTION = 'The option entered is not valid.'
NMAP_NOT_INSTALLED = 'Nmap is not installed.'
NMAP_IPV4_REGEX_RANGE = r"^(?:\d{1,3}\.){3}\d{1,3}\-\d{1,3}$"
INVALID_NMAP_IPV4_RANGE = 'The IPv4 range entered is not valid.'


def is_ipv4(ip):
    return re.match(IPV4_REGEX, ip)

def is_ipv4_range(ip_range):
    return re.match(IPV4_RANGE_REGEX, ip_range)

def is_port(port):
    return port.isdigit() and PORT_MIN <= int(port) <= PORT_MAX

def is_port_range(port_range):
    return re.match(PORT_RANGE_REGEX, port_range)

def is_nmap_ipv4_range(ip_range):
    return re.match(NMAP_IPV4_REGEX_RANGE, ip_range)

def is_nmap_installed():
    return os.path.exists('/usr/bin/nmap')


def scan_with_python_ipv4(ip, port_range):
    if is_ipv4(ip):
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
            port_range = [port_range[0], port_range[0]]
        open_ports = []
        for port in range(int(port_range[0]), int(port_range[1]) + 1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append((ip, port))
            s.close()
        result =  ', '.join(['{} {}:{}'.format((OPEN_PORTS), ip, port) for (ip, port) in open_ports])

        if result == '':
           return 'No open ports in {ip}'.format(ip=ip, port=port)
        else:
            return result

    elif is_ipv4_range(ip):
        ip_range = ip.split('-')
        ip_range = [ip_range[0].split('.'), ip_range[1].split('.')]
        if len(ip_range) == 1:
            ip_range = [ip_range[0], ip_range[0]]
        open_ports = []
        for ip in range(int(ip_range[0][0]), int(ip_range[1][0]) + 1):
            for ip2 in range(int(ip_range[0][1]), int(ip_range[1][1]) + 1):
                for ip3 in range(int(ip_range[0][2]), int(ip_range[1][2]) + 1):
                    for ip4 in range(int(ip_range[0][3]), int(ip_range[1][3]) + 1):
                        ip = '{ip}.{ip2}.{ip3}.{ip4}'.format(ip=ip, ip2=ip2, ip3=ip3, ip4=ip4)
                        if is_ipv4(ip):
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
                                port_range = [port_range[0], port_range[0]]
                            for port in range(int(port_range[0]), int(port_range[1]) + 1):
                                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                s.settimeout(0.1)
                                result = s.connect_ex((ip, port))
                                if result == 0:
                                    open_ports.append((ip, port))
                                s.close()
            result =  ', '.join(['{} {}:{}'.format((OPEN_PORTS), ip, port) for (ip, port) in open_ports])
            if result == '':
                return "No open ports in the specified IP range and port range."
            else:
                return result
    else:
        return INVALID_IPV4


def scan_with_nmap_ipv4(ip_range, port_range):
    if not is_nmap_installed():
        return NMAP_NOT_INSTALLED
    
    if '-' in ip_range:
        if not is_nmap_ipv4_range(ip_range):
            return INVALID_NMAP_IPV4_RANGE
    else:
        if not is_ipv4(ip_range):
            return INVALID_IPV4
        
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

    command = ['nmap', '-Pn', '-p', port_range, ip_range]
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
    
#Librerias
import re
import socket

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
        open_ports = []
        port_range = range(int(port_range[0]), int(port_range[1]) + 1)
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
        result =  ', '.join(['{} {}:{}'.format((OPEN_PORTS), ip, port) for (ip, port) in open_ports])
        if result == '':
            return "No open ports in the specified IP range and port range."
        else:
            return result
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