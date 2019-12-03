import socket
import sys
import time

class IRC:
 
    irc = socket.socket()
  
    def __init__(self):
        # Define the socket
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    def send(self, channel, msg):
        # Transfer data
        self.irc.send(bytes("PRIVMSG " + channel + " " + msg + "\n", "UTF-8"))
 
    def connect(self, server, port, channel, botnick):
        # Connect to the server
        print("Connecting to: " + server)
        self.irc.connect((server, port))

        # Perform user authentication
        self.irc.send(bytes("USER " + botnick + " " + botnick +" " + botnick + " :python\n", "UTF-8"))
        self.irc.send(bytes("NICK " + botnick + "\n", "UTF-8"))
        
        time.sleep(1)

        # join the channel
        self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))

        print("Most likely authenticated...")
 
    def get_response(self):
        time.sleep(1)
        # Get the response
        resp = self.irc.recv(2040).decode("UTF-8")

        print("Got some response")
 
        if resp.find('PING') != -1:
            print("Received PING")                      
            self.irc.send(bytes('PONG ' + resp.split().decode("UTF-8") [1] + '\r\n', "UTF-8")) 
 
        return resp


## IRC Config
server = "irc.urbelis.dev"
port = 3456
channel = "#test"
botnick = "PROBot"
irc = IRC()
irc.connect(server, port, channel, botnick)

while True:
    text = irc.get_response()
    print(text)
    
    if "PRIVMSG" in text and channel in text and "hello" in text:
        irc.send(channel, "Fuck!")