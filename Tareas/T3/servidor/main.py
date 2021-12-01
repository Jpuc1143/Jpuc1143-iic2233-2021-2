from socket import socket
from server import Server

print("starting server")
sock = socket()
sock.bind(("localhost", 8080))
sock.listen()
server = Server(sock.accept()[0])
server.join()
print("terminando programa")
