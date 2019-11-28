import socket
import time
from threading import Thread

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "10.0.42.17"
port = 65459
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host, port))
socket_list = []
client_list = []
channel_list = ["#test"]

class client(Thread):

    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.nick = ""
        self.user = ""
        self.channel = ""
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
            while self.nick == "" and self.user == "":
                
                while self.user == "":
                    message = self.sock.recv(2 ** 10).decode()
                    #print("The message is: " + message)

                    for line in message.splitlines():
                        print(line)
                        messageParsed = line.split(' ')
                        if(messageParsed[0] == "NICK"):
                            if(messageParsed[1] != ""):
                               self.nick = messageParsed[1]
                            else:
                                self.sock.send(b'Invalid Paramater for NICK')

                        if(messageParsed[0] == "USER"):
                            if(messageParsed[1] != ""):
                                self.user = messageParsed[1]
                            else:
                                self.sock.send(b'Invalid Paramater for USER')

                        if(messageParsed[0] == "QUIT"):
                            self.sock.close()
                            return
                    
            print("User: " + self.user + " Nick: " + self.nick)
            if(self.nick != "" and self.user != ""):
                print("Adding user to list")
                global socket_list
                socket_list.append(self.sock)
                global client_list
                client_list.append(self.user)
                print("Added to user list.")
                for users in client_list:
                    print(users)

            print("TEST")

            while True:
                print("TESTING")
                message = self.sock.recv(1024).decode()
                print("Test1")
                messageParsed = message.split(' ')
                print(message)
                if(messageParsed[0] == "JOIN"):
                    print("Test2")
                    for channel in channel_list:
                        print("Test3")
                        print(messageParsed[1])
                        print(channel)
                        if(messageParsed[1] == channel):
                            self.channel = channel
                            print("Test4")




                
                #     messageSend = 'Welcome to the IRC! ' + self.nick + ':' + self.user

                #     self.sock.send(messageSend.encode())
                #     tm = time.strftime('%H:%M:%S')
                #     print(self.nick + ":" + self.user + " Has connected to the server at: " + tm)
                # else:
                #     self.sock.send(b"Receieved by server")
                
                # print("User " + self.nick + " connected. " + self.user)

serversocket.listen(5)
print("Server started and Listening")

while True:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)

