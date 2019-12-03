import socket
import sys
import time
import datetime
from datetime import datetime

class IRC:
 
    irc = socket.socket()
  
    def __init__(self):
        # Define the socket
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    def send(self, channel, msg):
        # Transfer data
        self.irc.send(("PRIVMSG " + channel + " " + msg + "\n").encode())
 
    def connect(self, server, port, channel, botnick, botuser):
        # Connect to the server
        print("Connecting to: " + server)
        self.irc.connect((server, port))

        # Perform user authentication
        self.irc.sendall(("USER " + botuser + "\n").encode())
        self.irc.sendall(("NICK " + botnick + "\n").encode())
        
        time.sleep(1)

        # join the channel
        self.irc.sendall(("JOIN " + channel + "\n").encode())

        print("Most likely authenticated...")
 
    def get_response(self):
        time.sleep(5)
        # Get the response
        resp = self.irc.recv(2 ** 10).decode()

        print("Got some response " + resp)
 
        if resp.find('PING') != -1:
            print("Received PING")                      
            self.irc.send(('PONG ' + resp.split() [1] + '\r\n').encode()) 
 
        return resp


## IRC Config
server = "10.0.42.17"
port = 3456
channel = "#test"
botnick = "PROBot"
botuser = "PROBotUsername"
irc = IRC()
irc.connect(server, port, channel, botnick, botuser)

while True:
    text = irc.get_response()
    print(text)

    today = datetime.today()
     
    if "PRIVMSG" in text and channel in text and "!day" in text:
        irc.send(channel, datetime.today().strftime('%A'))

    if "PRIVMSG" in text and channel in text and "!time" in text:
        irc.send(channel, datetime.today().strftime('%X'))