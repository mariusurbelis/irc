#! /usr/bin/python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "irc.urbelis.dev"
port = 3456
s.connect((host, port))

s.sendall("CAP LS 302\n".encode())
s.sendall("NICK ProBot\n".encode())
s.sendall("USER ProBot\n".encode())

s.sendall("JOIN #test\n".encode())

while True:
    i = 1

s.close()
