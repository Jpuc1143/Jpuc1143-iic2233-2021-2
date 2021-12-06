from socket import socket
from server_connection import ServerConnection

print("starting server")
sock = socket()
sock.bind(("localhost", 8080))
sock.listen()
while True:
    server_connection = ServerConnection(sock.accept()[0])
    # server.join()

print("terminando programa")
