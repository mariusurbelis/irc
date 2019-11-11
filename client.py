#! /usr/bin/python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host ="127.0.0.1"
port = 65432
s.connect((host,port))

username = input('Please enter a username: ')

def ts(r):
   message1 = username + ":" + r
   message2 = bytes(message1, 'utf-8')
   s.sendall(message2)
   data = s.recv(1024).decode()
   print (data)

while 2:
   r = input('Enter: ')
   ts(r)

s.close ()