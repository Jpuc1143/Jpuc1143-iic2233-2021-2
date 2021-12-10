from socket import socket
from server_connection import ServerConnection
from dccalamar import DCCalamar
from parameters import Parameters as p

print("starting server")
sock = socket()
sock.bind((p.host, p.port))
sock.listen()
server = DCCalamar()

while True:
    server_connection = ServerConnection(sock.accept()[0], server)
    # server.join()

print("terminando programa")
