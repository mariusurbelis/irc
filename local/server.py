import socket
from threading import Thread

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "10.0.42.17"
port = 65432
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host, port))
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
        try:
            #While username and nickname not set
            while self.nick == "" and self.user == "":
                
                while self.user == "":
                    message = self.sock.recv(2 ** 10).decode()

                    for line in message.splitlines():
                        print(line)
                        messageParsed = line.split(' ')
                        if(messageParsed[0] == "NICK"):
                            if(messageParsed[1] != ""):
                                global client_list
                                for client in client_list:
                                    if messageParsed[1] == client.nick:
                                        message = self.user + ' ' + messageParsed[1] + ':Nickname is already in use\n'
                                        self.sock.send(message.encode())
                                        return
                                self.nick = messageParsed[1]
                            else:
                                self.sock.send(b'Invalid Paramater for NICK')

                        if(messageParsed[0] == "USER"):
                            if(messageParsed[1] != ""):
                                self.user = messageParsed[1]
                            else:
                                self.sock.send(b'Invalid Paramater for USER')


            print("User: " + self.user + " Nick: " + self.nick)
            if(self.nick != "" and self.user != ""):
                print("Adding " + self.user + " to client list")
                client_list.append(self)

                for users in client_list:
                    print(users)

                REPLY_001 = ':10.0.42.17 001 ' + self.user + ' :Welcome to the IRC server!\n'
                REPLY_002 = ':10.0.42.17 002 ' + self.user + ' :Your host is ' + 'labpc213\n'
                REPLY_003 = ':10.0.42.17 003 ' + self.user + ' :This server was created ..\n'

                message = REPLY_001 + REPLY_002 + REPLY_003 
                self.sock.send(message.encode())
  
            while True:
                message = self.sock.recv(1024).decode()
                for line in message.splitlines():
                    messageParsed = line.split(' ')

                    #Join channel protocol
                    if(messageParsed[0] == "JOIN"):
                        for channel in channel_list:
                            print(messageParsed[1])
                            if(messageParsed[1] == channel):
                                self.channel = channel
                                REPLY_331 = ':10.0.42.17 331 ' + self.user + ' ' + self.channel + ' :No topic is set\n'
                                REPLY_353 = ':10.0.42.17 353 ' + self.user + ' = ' +  self.channel + ' :'

                                for client in client_list:
                                    if(client.channel == self.channel):
                                        REPLY_353 = REPLY_353 + ' ' + client.user
                                REPLY_353 = REPLY_353 + '\n'

                                REPLY_366 = ':10.0.42.17 366 ' + self.user + ' ' + self.channel + ' :End of NAMES list\n'
                                REPLY = ':' + self.user + ' ' + line + '\n'
                                message = REPLY + REPLY_331 + REPLY_353 + REPLY_366

                                for client in client_list:
                                    if(client.channel == self.channel):
                                        client.sock.send(message.encode())

                    #Leave channel protocol
                    if(messageParsed[0] == "PART"):
                        if(self.channel != ""):
                            message = ':' + self.user + ' ' + line + '\n'
                            print(message)
                            for client in client_list:
                                    if(client.channel == self.channel):
                                        client.sock.send(message.encode())
                            self.channel = ""

                    #Leave server protocol
                    if(messageParsed[0] == "QUIT"):
                        if(self.channel != ""):
                            message = ':' + self.user + ' ' + line + '\n'
                            print(message)
                            for client in client_list:
                                    if(client.channel == self.channel):
                                        client.sock.send(message.encode())
                            self.channel = ""

                    #Message protocol
                    if(messageParsed[0] == "PRIVMSG"):
                        for client in client_list:

                            #Message Channel
                            if(client.channel == self.channel):
                                if (client != self):
                                    message = ':' + self.nick + '!' + self.user + '@somecunt ' + line + '\n'
                                    client.sock.send(message.encode())

                            #Message User
                            elif(messageParsed[1] == client.user):
                                if(messageParsed[2] != ":"):
                                    message = ':' + self.nick + '!' + self.user + '@somecunt ' + line + '\n'
                                    client.sock.send(message.encode())
        except socket.error:
            #If socket error, remove client from list then close socket connection
            client_list.remove(self)
            self.sock.close()

#Listen for client connections to server
serversocket.listen(5)
print("Server started and Listening")

while True:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)

