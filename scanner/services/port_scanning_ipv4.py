import socket, re, os
from subprocess import getoutput, Popen, PIPE
from .services_constants import *


def is_ipv4(ip):
    return re.match(IPV4_REGEX, ip)

def is_ipv4_domain(ip):
    try:
        ip = socket.gethostbyname(ip)
        return True, ip
    except socket.gaierror:
        return False

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

def scan_ipv4(ip, port_range):
    open_ports = []
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
        return NOT_OPEN_PORTS
    else:
        return result

def ipv4_range_ip_setup(ip):
    ip_range = ip.split('-')
    ip_range = [ip_range[0].split('.'), ip_range[1].split('.')]
    if len(ip_range) == 1:
        ip_range = [ip_range[0], ip_range[0]]
    for ip in range(int(ip_range[0][0]), int(ip_range[1][0]) + 1):
        for ip2 in range(int(ip_range[0][1]), int(ip_range[1][1]) + 1):
            for ip3 in range(int(ip_range[0][2]), int(ip_range[1][2]) + 1):
                for ip4 in range(int(ip_range[0][3]), int(ip_range[1][3]) + 1):
                    ip = '{ip}.{ip2}.{ip3}.{ip4}'.format(ip=ip, ip2=ip2, ip3=ip3, ip4=ip4)
                    yield ip

def scan_with_python_ipv4(ip, port_range):
    #Verificamos si es por ipv4, dominio o rango
    if '-' in ip:
        if not is_ipv4_range(ip):
            return INVALID_IPV4_RANGE
        else:
            for ip in ipv4_range_ip_setup(ip):
                return scan_ipv4(ip, port_range)
    else:
        if not is_ipv4(ip):
            if not is_ipv4_domain(ip):
                return INVALID_IPV4_DOMAIN
            else:
                ip = is_ipv4_domain(ip)[1]
        return scan_ipv4(ip, port_range)
    
    
def scan_nmap(ip_range, port_range):
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
    

def scan_with_nmap_ipv4(ip_range, port_range):
    if not is_nmap_installed():
        return NMAP_NOT_INSTALLED
    
    if '-' in ip_range:
        print('llega')
        if not is_nmap_ipv4_range(ip_range):
            return INVALID_NMAP_IPV4_RANGE
        else:
            scan = scan_nmap(ip_range, port_range)
            print('llega')
            return scan
    else:
        if not is_ipv4(ip_range):
            if not is_ipv4_domain(ip_range):
                print('llega')
                return NMAP_INVALID_DOMAIN
            else:
                ip_range = is_ipv4_domain(ip_range)[1]
        return scan_nmap(ip_range, port_range)
        
        

def main():
    print('''
    1. Escanear con python
    2. Escanear con nmap
    ''')
    option = input('Elija una opcion: ')
    if option == '1':
        ip = input('Ingrese la ip: ')
        port_range = input('Ingrese el rango de puertos: ')
        scan = scan_with_python_ipv4(ip, port_range)
        print(scan)
    elif option == '2':
        ip_range = input('Ingrese el rango de ips: ')
        port_range = input('Ingrese el rango de puertos: ')
        scan = scan_with_nmap_ipv4(ip_range, port_range)
        print(scan)
    else:
        print('Opcion invalida')
        main()

if __name__ == '__main__':
    main()
