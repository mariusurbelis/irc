#! /usr/bin/python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 3456
s.connect((host, port))

# Print server's welcome message
print("\n-------------------")
print(s.recv(1024).decode())
print("-------------------\n")

username = input('Choose your username: ')
s.sendall(bytes(username, 'utf-8'))

def ts(r):
    message2 = bytes(r, 'utf-8')
    s.sendall(message2)

while True:
    r = input('> ')
    ts(r)

s.close()
