import socket
from threading import Thread

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 80
serversocket.bind((host, port))

class client(Thread):

    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()
        # Sending the welcome message for every new client
        self.sock.send(str.encode("Welcome to the IRC\n1. Be nice\n2. Choose a username"))

    def run(self):
        username = ""
        initial = 0
        while True:
            if initial == 0:
                username = self.sock.recv(1024).decode()
                print ("\n<> " + username + " connected <>")
                initial = 1
            else:
                data = self.sock.recv(1024).decode()
                if not data:
                    print ("\nX " + username + " disconnected X")
                    return
                print("\n> " + username + " says " + data)

serversocket.listen(5)
print("Server started and Listening")

while True:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)