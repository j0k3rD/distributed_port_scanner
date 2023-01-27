import socket, re, os, sys, time, threading, queue, time, datetime, subprocess, platform, ipaddress
from constants import *

# Functions
def is_ipv4(ip):
    return re.match(IPV4_REGEX, ip)

def is_ipv4_range(ip_range):
    return re.match(IPV4_RANGE_REGEX, ip_range)

def get_ipv4_range(ip_range):
    ip_min, ip_max = ip_range.split('-')
    ip_min_list = ip_min.split('.')
    ip_max_list = ip_max.split('.')
    ip_range_list = []
    for oct1 in range(int(ip_min_list[0]), int(ip_max_list[0])+1):
        for oct2 in range(int(ip_min_list[1]), int(ip_max_list[1])+1):
            for oct3 in range(int(ip_min_list[2]), int(ip_max_list[2])+1):
                for oct4 in range(int(ip_min_list[3]), int(ip_max_list[3])+1):
                    ip_range_list.append('{}.{}.{}.{}'.format(oct1, oct2, oct3, oct4))
    return ip_range_list

def is_port_range(port_range):
    return re.match(PORT_RANGE_REGEX, port_range)

def get_port_range(port_range):
    port_min, port_max = port_range.split('-')
    return range(int(port_min), int(port_max)+1)

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((ip, port))
    if result == 0:
        return True
    else:
        return False

def scan_ipv4(ip, port_range):
    port_range = _get_port_range(port_range)
    open_ports = []
    for port in port_range:
        if _scan_port(ip, port):
            open_ports.append(port)
    return open_ports

def scan_ipv4_range(ip_range, port_range):
    ip_range = _get_ipv4_range(ip_range)
    port_range = _get_port_range(port_range)
    open_ports = {}
    for ip in ip_range:
        open_ports[ip] = []
        for port in port_range:
            if _scan_port(ip, port):
                open_ports[ip].append(port)
    return open_ports

def scan_with_nmap(ip, port_range):
    os.system('nmap -p {} {}'.format(port_range, ip))

def scan_with_python(ip, port_range):
    if _is_ipv4(ip):
        open_ports = _scan_ipv4(ip, port_range)
        print(OPEN_PORTS.format(ip=ip, open_ports=open_ports))
    elif _is_ipv4_range(ip):
        open_ports = _scan_ipv4_range(ip, port_range)
        for ip, ports in open_ports.items():
            print(OPEN_PORTS.format(ip=ip, open_ports=ports))
    else:
        print(INVALID_IPV4)

def main():
    ip = input(IPV4_INPUT)
    port_range = input(PORT_INPUT)
    option = input(PYTHON_OR_NMAP)
    if option == '1':
        scan_with_python(ip, port_range)
    elif option == '2':
        scan_with_nmap(ip, port_range)
    else:
        print(INVALID_OPTION)

if __name__ == '__main__':
    main()