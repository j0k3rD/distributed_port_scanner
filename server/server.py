#Servidor 
import socketserver
from tasks import scan_ports_python

from celery.result import AsyncResult

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        ipv4 = self.data.decode('utf-8')
        for port in range(1, 1024):
            scan_ports_python.delay(ipv4, port)
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()