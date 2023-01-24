import socket, re, os

# Constants
IPV4_REGEX = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
PORT_RANGE_REGEX = r"^(?:(?:[0-9]{1,4})-(?:[0-9]{1,4}))$"
PORT_MIN = 1
PORT_MAX = 65535
IPV4_RANGE_REGEX = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)-(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

# Functions

def nmap_scan(ip, port_range):
    os.system("nmap -sT -p " + port_range + " " + ip)

def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def is_ipv4(ip):
    return re.match(IPV4_REGEX, ip)

def is_ipv4_range(ip_range):
    return re.match(IPV4_RANGE_REGEX, ip_range)

def get_ipv4_range(ip_range):
    ip_range = ip_range.split("-")
    ip_range = list(map(int, ip_range))
    return ip_range

def is_port_range(port_range):
    return re.match(PORT_RANGE_REGEX, port_range)

def get_port_range(port_range):
    port_range = port_range.split("-")
    port_range = list(map(int, port_range))
    return port_range

def get_open_ports(ip, port_range):
    open_ports = []
    for port in range(port_range[0], port_range[1] + 1):
        print_progress_bar(port, port_range[1], prefix = 'Progress:', suffix = 'Complete', length = 50)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def save_scan(ip, open_ports):
    for port in open_ports:
        os.system("python save_scan.py " + ip + " " + str(port))

# Main
if __name__ == "__main__":
    #Printear todos los puertos testeados y los que estan abiertos
    scan_method = input("Enter the scan method (1: nmap, 2: python): ")
    if scan_method == "1":
        ip = input("Enter the IP address: ")
        if is_ipv4(ip):
            port_range = input("Enter the port range (ex: 1-65535): ")
            if is_port_range(port_range):
                port_range = get_port_range(port_range)
                if port_range[0] >= PORT_MIN and port_range[1] <= PORT_MAX:
                    open_ports = get_open_ports(ip, port_range)
                    print(open_ports)
                    save_scan(ip, open_ports)
                else:
                    print("Port range must be between " + str(PORT_MIN) + " and " + str(PORT_MAX))
            else:
                print("Port range must be in the format 1-65535")
        elif is_ipv4_range(ip):
            ip_range = get_ipv4_range(ip)
            port_range = input("Enter the port range (ex: 1-65535): ")
            if is_port_range(port_range):
                port_range = get_port_range(port_range)
                if port_range[0] >= PORT_MIN and port_range[1] <= PORT_MAX:
                    for ip in range(int(ip_range[0].split(".")[3]), int(ip_range[1].split(".")[3]) + 1):
                        ip = ip_range[0].split(".")[0] + "." + ip_range[0].split(".")[1] + "." + ip_range[0].split(".")[2] + "." + str(ip)
                        print("Scanning " + ip)
                        open_ports = get_open_ports(ip, port_range)
                        print(open_ports)
                        save_scan(ip, open_ports)
                else:
                    print("Port range must be between " + str(PORT_MIN) + " and " + str(PORT_MAX))
            else:
                print("Port range must be in the format 1-65535")
        else:
            print("Invalid IP address")

    elif scan_method == "2":
        ip = input("Enter the IP address: ")
        if is_ipv4(ip):
            port_range = input("Enter the port range (ex: 1-65535): ")
            if is_port_range(port_range):
                port_range = get_port_range(port_range)
                if port_range[0] >= PORT_MIN and port_range[1] <= PORT_MAX:
                    nmap_scan(ip, port_range)
                else:
                    print("Port range must be between " + str(PORT_MIN) + " and " + str(PORT_MAX))
            else:
                print("Port range must be in the format 1-65535")
        elif is_ipv4_range(ip):
            ip_range = get_ipv4_range(ip)
            port_range = input("Enter the port range (ex: 1-65535): ")
            if is_port_range(port_range):
                port_range = get_port_range(port_range)
                if port_range[0] >= PORT_MIN and port_range[1] <= PORT_MAX:
                    for ip in range(int(ip_range[0].split(".")[3]), int(ip_range[1].split(".")[3]) + 1):
                        ip = ip_range[0].split(".")[0] + "." + ip_range[0].split(".")[1] + "." + ip_range[0].split(".")[2] + "." + str(ip)
                        print("Scanning " + ip)
                        nmap_scan(ip, port_range)
                else:
                    print("Port range must be between " + str(PORT_MIN) + " and " + str(PORT_MAX))
            else:
                print("Port range must be in the format 1-65535")
        else:
            print("Invalid IP address")
    
    else:
        print("Invalid scan method")