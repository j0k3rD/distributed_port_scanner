#Guardar el resultado del escaneo en base de datos

import mysql.connector
import sys

#Conectar a la base de datos
mydb = mysql.connector.connect( host="localhost",
                                user="root",
                                password="root",
                                database="port_scanning" )

#Crear cursor
mycursor = mydb.cursor()

#Crear tabla
mycursor.execute("CREATE TABLE IF NOT EXISTS port_scanning (id INT AUTO_INCREMENT PRIMARY KEY, ip VARCHAR(255), port VARCHAR(255))")

#Guardar los datos en la base de datos
ip = sys.argv[1]
port = sys.argv[2]
sql = "INSERT INTO port_scanning (ip, port) VALUES (%s, %s)"
val = (ip, port)
mycursor.execute(sql, val)
mydb.commit()

#Cerrar conexion
mydb.close()


# # Main
# if __name__ == "__main__":
#     #Printear todos los puertos testeados y los que estan abiertos
#     ip = input("Enter the IP address: ")
#     if is_ipv4(ip):
#         port_range = input("Enter the port range (ex: 1-65535): ")
#         if is_port_range(port_range):
#             port_range = get_port_range(port_range)
#             if port_range[0] >= PORT_MIN and port_range[1] <= PORT_MAX:
#                 open_ports = get_open_ports(ip, port_range)
#                 print(open_ports)
#                 save_scan(ip, open_ports)
#             else:
#                 print("Port range must be between " + str(PORT_MIN) + " and " + str(PORT_MAX))
#         else:
#             print("Port range must be in the format 1-65535")
#     elif is_ipv4_range(ip):
#         ip_range = get_ipv4_range(ip)
#         port_range = input("Enter the port range (ex: 1-65535): ")
#         if is_port_range(port_range):
#             port_range = get_port_range(port_range)
#             if port_range[0] >= PORT_MIN and port_range[1] <= PORT_MAX:
#                 for ip in range(int(ip_range[0].split(".")[3]), int(ip_range[1].split(".")[3]) + 1):
#                     ip = ip_range[0].split(".")[0] + "." + ip_range[0].split(".")[1] + "." + ip_range[0].split(".")[2] + "." + str(ip)
#                     print("Scanning " + ip)
#                     open_ports = get_open_ports(ip, port_range)
#                     print(open_ports)
#                     save_scan(ip, open_ports)
#             else:
#                 print("Port range must be between " + str(PORT_MIN) + " and " + str(PORT_MAX))
#         else:
#             print("Port range must be in the format 1-65535")
#     else:
#         print("Invalid IP address")


import socket, re, os

# Constants
IPV4_REGEX = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
PORT_RANGE_REGEX = r"^(?:(?:[0-9]{1,4})-(?:[0-9]{1,4}))$"
PORT_MIN = 1
PORT_MAX = 65535
IPV4_RANGE_REGEX = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)-(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

# Functions

## Preguntar si se desea escanear con python o con nmap
## Preguntar si se desea escanear una ipv4 o un rango de ipv4
## Agregar barras de progreso
## Agregar tiempo de espera
## Ir printeando los puertos abiertos encontrados

# def is_ipv4(ip):
#     return re.match(IPV4_REGEX, ip)

# def is_ipv4_range(ip_range):
#     return re.match(IPV4_RANGE_REGEX, ip_range)

# def get_ipv4_range(ip_range):
#     ip_min, ip_max = ip_range.split('-')
#     ip_min_list = ip_min.split('.')
#     ip_max_list = ip_max.split('.')
#     ip_range_list = []
#     for oct1 in range(int(ip_min_list[0]), int(ip_max_list[0])+1):
#         for oct2 in range(int(ip_min_list[1]), int(ip_max_list[1])+1):
#             for oct3 in range(int(ip_min_list[2]), int(ip_max_list[2])+1):
#                 for oct4 in range(int(ip_min_list[3]), int(ip_max_list[3])+1):
#                     ip_range_list.append('{}.{}.{}.{}'.format(oct1, oct2, oct3, oct4))
#     return ip_range_list

# def is_port_range(port_range):
#     return re.match(PORT_RANGE_REGEX, port_range)

# def get_port_range(port_range):
#     port_min, port_max = port_range.split('-')
#     return range(int(port_min), int(port_max)+1)

# def scan_port(ip, port):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.settimeout(0.5)
#     result = sock.connect_ex((ip, port))
#     if result == 0:
#         return True
#     else:
#         return False

# def scan_ipv4(ip, port_range):
#     port_range = get_port_range(port_range)
#     open_ports = []
#     for port in port_range:
#         if scan_port(ip, port):
#             open_ports.append(port)
#     return open_ports

# def scan_ipv4_range(ip_range, port_range):
#     ip_range = get_ipv4_range(ip_range)
#     port_range = get_port_range(port_range)
#     open_ports = {}
#     for ip in ip_range:
#         open_ports[ip] = []
#         for port in port_range:
#             if scan_port(ip, port):
#                 open_ports[ip].append(port)
#     return open_ports

# def scan_with_nmap(ip, port_range):
#     os.system('nmap -p {} {}'.format(port_range, ip))

# def scan_with_python(ip, port_range):
#     if is_ipv4(ip):
#         open_ports = scan_ipv4(ip, port_range)
#         print('Puertos abiertos en {}: {}'.format(ip, open_ports))
#     elif is_ipv4_range(ip):
#         open_ports = scan_ipv4_range(ip, port_range)
#         for ip in open_ports:
#             print('Puertos abiertos en {}: {}'.format(ip, open_ports[ip]))
#     else:
#         print('La ip ingresada no es válida')

# def main():
#     print('''
#     1. Escanear con python
#     2. Escanear con nmap
#     ''')
#     option = input('Ingrese una opción: ')
#     if option == '1':
#         ip = input('Ingrese una ip o un rango de ips: ')
#         port_range = input('Ingrese un rango de puertos: ')
#         scan_with_python(ip, port_range)
#     elif option == '2':
#         ip = input('Ingrese una ip: ')
#         port_range = input('Ingrese un rango de puertos: ')
#         scan_with_nmap(ip, port_range)
#     else:
#         print('La opción ingresada no es válida')

# if __name__ == '__main__':
#     main()