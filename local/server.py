import socket
import time
from threading import Thread

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "10.0.42.17"
port = 65432
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

                message1 = ':10.0.42.17 001 ' + self.user + ' :Welcome to the IRC server!\n'
                message2 = ':10.0.42.17 002 ' + self.user + ' :Your host is ' + 'labpc213\n'
                message3 = ':10.0.42.17 003 ' + self.user + ' :This server was created ...\n'

                message = message1 + message2 + message3 
                messageEncoded = message.encode()
                self.sock.send(messageEncoded)
                



                

            while True:
                message = self.sock.recv(1024).decode()
                for line in message.splitlines():
                    messageParsed = line.split(' ')
                    if(messageParsed[0] == "JOIN"):
                        for channel in channel_list:
                            print(messageParsed[1])
                            print(channel)
                            if(messageParsed[1] == channel):
                                self.channel = channel
                                message1 = ':10.0.42.17 331 ' + self.user + ' ' + self.channel + ' :No topic is set\n'
                                message2 = ':10.0.42.17 353 ' + self.user + ' = ' +  self.channel + ' :' + self.user + '\n'
                                message3 = ':10.0.42.17 366 ' + self.user + ' ' + self.channel + ' :End of NAMES list\n'
                                #message4 = self.user + ' ' + line
                                message4 = ':' + self.user + ' ' + line + '\n'
                                print(message4)
                                message = message4 + message1 + message2 + message3 
                                messageEncoded = message.encode()
                                self.sock.send(messageEncoded)

                
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

