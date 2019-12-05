import socket
from threading import Thread
import threading
import time
import platform

# Creating the socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "10.0.42.17"
# host = ""
port = 3456
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host, port))
# Prepare the initial client list
client_list = []
# Prepare the initial channel list
channel_list = ["#test", "#general"]


# ----- NOT IMPLIMENTED -----
# Ping function sends a ping to users
# def ping():
#     print("Pinging")
#     for client in client_list:
#         print("Found a user " + client.user)
#         ping = 'PING ' + client.user + '\n'
#         client.sock.send(ping.encode())
#         resp = client.sock.recv(2 ** 10).decode()
#         if("PONG" not in resp):
#             #For each client, send message that user has quit
#             for client2 in client_list:
#                 message = ':' + client.nick + "!" + client.user + '@' + platform.node() + ' QUIT ' + client.nick + '\n'
#                 client2.sock.send(message.encode())
#             #Remove user from list of clients and then close the socket
#             client_list.remove(client)
#             client.sock.close()



# The client class
class client(Thread):
    # Constructor for the client class
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.nick = ""
        self.user = ""
        self.channel = []
        self.start()

    def run(self):
        try:
            #While username and nickname not set
            while self.nick == "" and self.user == "":
                
                while self.user == "":
                    # Read received data
                    message = self.sock.recv(2 ** 10).decode()

                    for line in message.splitlines():
                        # print(line)
                        messageParsed = line.split(' ')
                        # Check if the client is sending a nickname parameter
                        if(messageParsed[0] == "NICK"):
                            if(messageParsed[1] != ""):
                                global client_list
                                for client in client_list:
                                    # If a nickname already exists, inform the user
                                    if messageParsed[1] == client.nick:
                                        message = self.nick + ' ' + messageParsed[1] + ':Nickname is already in use\n'
                                        self.sock.send(message.encode())
                                        self.sock.close()
                                        return
                                self.nick = messageParsed[1]
                            else:
                                self.sock.send(b'Invalid Paramater for NICK')

                        # Check if the client is sending a username parameter
                        if(messageParsed[0] == "USER"):
                            if(messageParsed[1] != ""):
                                self.user = messageParsed[1]
                            else:
                                self.sock.send(b'Invalid Paramater for USER')

            print("User: " + self.user + " Nick: " + self.nick)
            if(self.nick != "" and self.user != ""):
                print("Adding " + self.user + " to client list")
                client_list.append(self)

                # Constructing and sending the initial welcome messages
                REPLY_001 = ':' + host + ' 001 ' + self.nick + ' :Welcome to the IRC server!\n'
                REPLY_002 = ':' + host + ' 002 ' + self.nick + ' :Your host is ' + 'Nox\n'
                REPLY_003 = ':' + host + ' 003 ' + self.nick + ' :This server was created ..\n'
                message = REPLY_001 + REPLY_002 + REPLY_003 + "Join general by typing /join #general\n"
                                
                self.sock.send(message.encode())
  
            while True:

                message = self.sock.recv(1024).decode()
                for line in message.splitlines():
                    messageParsed = line.split(' ')

                    #Join channel protocol
                    if(messageParsed[0] == "JOIN"):
                        found = False
                        for channel in channel_list:
                            if(messageParsed[1] == channel):
                                found = True
                        channel = messageParsed[1]

                        #If channel not found, create channel with name
                        if(not found):
                            channel_list.append(channel)
                            found = True

                        #If channel found, send reply codes and broadcast to everyone in channel
                        if (found):
                            self.channel.append(channel)
                            REPLY_331 = ':' + host + ' 331 ' + self.nick + ' ' + channel + ' :No topic is set\n'
                            REPLY_353 = ':' + host + ' 353 ' + self.nick + ' = ' + channel + ' :'

                            #Add every client in channel to list of users
                            for client in client_list:
                                for clientChannel in client.channel:
                                    if(clientChannel == channel):
                                        REPLY_353 = REPLY_353 + ' ' + client.nick
                            REPLY_353 = REPLY_353 + '\n'

                            REPLY_366 = ':' + host + ' 366 ' + self.nick + ' ' + channel + ' :End of NAMES list\n'
                            REPLY = ':' + self.nick + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                            message = REPLY + REPLY_331 + REPLY_353 + REPLY_366
                            print(message)

                            #If client in channel, send message
                            for client in client_list:
                                for clientChannel in client.channel:
                                    if(clientChannel == channel):
                                        client.sock.send(message.encode())

                    #Leave channel protocol
                    if(messageParsed[0] == "PART"):
                        if(self.channel):
                            channel = messageParsed[1]
                            message = ':' + self.nick + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                            #For each client in channel, send message that user left
                            for client in client_list:
                                for clientChannel in client.channel:
                                    if(clientChannel == channel):
                                        client.sock.send(message.encode())
                            #Remove channel frm users channel list
                            self.channel.remove(channel)

                    #Leave server protocol
                    if(messageParsed[0] == "QUIT"):
                        #For each client, send message that user has quit
                        for client in client_list:
                            message = ':' + self.nick + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                            client.sock.send(message.encode())
                        #Remove user from list of clients and then close the socket
                        client_list.remove(self)
                        self.sock.close()

                    #Message protocol
                    if(messageParsed[0] == "PRIVMSG"):
                        channel = messageParsed[1]
                        for client in client_list:
                            
                            #Message Channel
                            for clientChannel in client.channel:
                                if(clientChannel == channel):
                                    if (client != self):
                                        message = ':' + self.nick + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                                        client.sock.send(message.encode())


                            #Message User
                            if(messageParsed[1] == client.nick):
                                if(messageParsed[2] != ":"):
                                    if(messageParsed[1] != self.nick):
                                        message = ':' + self.nick + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                                        client.sock.send(message.encode())

        except socket.error:
            #If socket error, remove client from list then close socket connection
            client_list.remove(self)
            self.sock.close()
            return

#Listen for client connections to server
serversocket.listen(5)
print("Server started and Listening")

while True:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
    
    # ----- NOT IMPLIMENTED -----
    # t = threading.Timer(5.0, lambda: ping())
    # t.daemon = True
    # t.start()
