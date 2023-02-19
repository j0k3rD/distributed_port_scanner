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