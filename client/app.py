import socket

def main():
    HOST, PORT = "localhost", 9999
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((HOST, PORT))
    msg = input("Ingrese una ipv4: ")
    socket.sendall(msg.encode('utf-8'))
    data = socket.recv(1024)
    print(data.decode('utf-8'))
    socket.close()

if __name__ == "__main__":
    main()