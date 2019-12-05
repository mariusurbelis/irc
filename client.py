import socket
import sys
import time
import datetime
import csv
import platform
from random import randint
tweets = []

class IRC:
 
    irc = socket.socket()
  
    def __init__(self):
        # Define the socket
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    def send(self, channel, msg):
        # Transfer data
        toSend = "PRIVMSG " + channel + " :" + msg + "\r\n"
        self.irc.send(toSend.encode())
 
    def connect(self, server, port, channel, botnick, botuser):
        # Connect to the server
        print("Connecting to: " + server)
        self.irc.connect((server, port))

        # Perform user authentication
        self.irc.sendall(("CAP LS 302\r\n").encode())
        self.irc.sendall(("USER " + botuser + " " + botuser + " 10.0.42.17 :realname\r\n").encode())
        self.irc.sendall(("NICK " + botnick + "\r\n").encode())
        
        time.sleep(1)

        # join the channel
        self.irc.sendall(("JOIN " + channel + "\n").encode())

        print("Most likely authenticated...")
 
    def get_response(self):
        # Get the response
        resp = self.irc.recv(2 ** 10).decode()

        print("Got some response " + resp)
 
        if resp.find('PING') != -1:
            print("Received PING")                      
            self.irc.send(('PONG ' + platform.node() + ' ' + server + '\r\n').encode()) 
 
        return resp


## IRC Config
server = "irc.urbelis.dev"
#server = "10.0.42.17"
port = 3456
channel = "#test"
botnick = "PROBot"
botuser = "PROBotUsername"
irc = IRC()
irc.connect(server, port, channel, botnick, botuser)


#Code to read in trump_tweets.csv and append to the tweets list
#Code taken from realypython.com/python-csv/
with open('trump_tweets.csv', encoding='utf-8', errors='ignore') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            tweets.append(row[1])
            line_count 
    print(f'Processed {line_count} lines.')

while True:
    text = irc.get_response()
    print(text)

    #gives the current day of the week
    if "PRIVMSG" in text and channel in text and "!day" in text:
        irc.send(channel, datetime.datetime.today().strftime('%A'))
    #gives current the time
    if "PRIVMSG" in text and channel in text and "!time" in text:
        irc.send(channel, datetime.datetime.today().strftime('%X'))
    #If messages not in the specified channel, message user with a trump tweet
    if "PRIVMSG" in text and channel not in text:
        parse = text.split(' ')[0]
        user = parse.split("!")[0]
        value = randint(1, 1928)
        irc.send(user.replace(':', ''), tweets[value])

