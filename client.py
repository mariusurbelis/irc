#! /usr/bin/python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host ="127.0.0.1"
port =65432
s.connect((host,port))

def ts(str):
   s.send(str.encode()) 
   data = ''
   data = s.recv(1024).decode()
   print (data)

while 2:
   r = input('Enter: ')
   ts(s)

s.close ()