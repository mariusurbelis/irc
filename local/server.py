import socket
import time
from threading import Thread

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 3456
serversocket.bind((host, port))


class client(Thread):


    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.nick = ""
        self.user = ""
        self.start()
        # Sending the welcome message for every new client
        # self.sock.send(str.encode("Welcome to the IRC\n1. Be nice\n2. Choose a username"))

    # def run(self):
    #     username = ""
    #     initial = 0
    #     while True:
    #         if initial == 0:
    #             username = self.sock.recv(1024).decode()
    #             print ("\n<> " + username + " connected <>")
    #             initial = 1
    #         else:
    #             data = self.sock.recv(1024).decode()
    #             if not data:
    #                 print ("\nX " + username + " disconnected X")
    #                 return
    #             print("\n> " + username + " says " + data)

    # def run(self):
    #     while True:
    #             print ("\n" + self.sock.recv(1024).decode())

    def run(self):
            while 1:
                message = self.sock.recv(1024).decode()
                print(message)
                messageParsed = message.splitlines()
                # messageParsed = message.split(" ")

                print("Line 1: " + messageParsed[0])


                if(messageParsed[0] == "NICK"):
                    if(messageParsed[1] != ""):
                        self.nick = messageParsed[1].splitlines()[0]
                    else:
                        self.sock.send(b'Invalid Paramater for NICK')


                elif(messageParsed[0] == "USER"):
                    if(messageParsed[1] != ""):
                        self.user = messageParsed[1]
                    else:
                        self.sock.send(b'Invalid Paramater for USER')


                # elif(messageParsed[0] == "PRIVMSG"):
                #     for users in clients:
                #         if(messageParsed[1] == users):
                #             if(messageParsed[2] != ""):
                #                 message = messageParsed[2].encode
                #                 self.sock.send(message)


                if(self.nick != "" and self.user != ""):
                    messageSend = 'Welcome to the IRC! ' + self.nick + ':' + self.user

                    self.sock.send(messageSend.encode())
                    tm = time.strftime('%H:%M:%S')
                    print(self.nick + ":" + self.user + " Has connected to the server at: " + tm)
                else:
                    self.sock.send(b"Receieved by server")
                
                print("User " + self.nick + " connected. " + self.user)

serversocket.listen(5)
print("Server started and Listening")

while True:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
