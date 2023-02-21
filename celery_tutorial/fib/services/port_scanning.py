import socket, re, os

# Constants
IPV4_REGEX = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
PORT_RANGE_REGEX = r"^(?:(?:[0-9]{1,4})-(?:[0-9]{1,4}))$"
PORT_MIN = 1
PORT_MAX = 65535
IPV4_RANGE_REGEX = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)-(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
IPV4_INPUT = 'Enter the IPv4 or IPv4 range to scan: '
PYTHON_OR_NMAP = '''Enter the option to scan:
                        1. Python
                        2. Nmap
'''
PORT_INPUT = 'Enter the port or port range to scan: '
OPEN_PORTS = 'Open ports in {ip}: {open_ports}'
SCANNING = 'Scanning...'
OPEN_PORT = 'The port {port} is open.'
INVALID_PORT = 'The port entered is not valid.'
INVALID_IPV4 = 'The IPv4 entered is not valid.'
INVALID_PORT_RANGE = 'The port range entered is not valid.'
INVALID_IPV4_RANGE = 'The IPv4 range entered is not valid.'
INVALID_OPTION = 'The option entered is not valid.'
NMAP_NOT_INSTALLED = 'Nmap is not installed.'


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
    port_range_list = []
    for port in range(int(port_min), int(port_max)+1):
        port_range_list.append(port)
    return port_range_list

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((ip, port))
    if result == 0:
        return True
    else:
        return False

def scan_ipv4(ip, port_range):
    port_range = get_port_range(port_range)
    open_ports = []
    for port in port_range:
        if scan_port(ip, port):
            open_ports.append(port)
    return open_ports

def scan_ipv4_range(ip_range, port_range):
    ip_range = get_ipv4_range(ip_range)
    port_range = get_port_range(port_range)
    open_ports = {}
    for ip in ip_range:
        open_ports[ip] = []
        for port in port_range:
            if scan_port(ip, port):
                open_ports[ip].append(port)
    return open_ports

def scan_with_python(ip, port_range):
    if is_ipv4(ip):
        open_ports = scan_ipv4(ip, port_range)
        return OPEN_PORTS.format(ip=ip, open_ports=open_ports)
    elif is_ipv4_range(ip):
        open_ports = scan_ipv4_range(ip, port_range)
        result = ""
        for ip, ports in open_ports.items():
            result += OPEN_PORTS.format(ip=ip, open_ports=ports) + "\n"
        return result
    else:
        return INVALID_IPV4

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