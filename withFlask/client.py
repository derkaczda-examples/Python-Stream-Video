import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code

socket_ip = '127.0.0.1'
cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect((socket_ip,8089))
while True:
    ret,frame=cap.read()
    data = pickle.dumps(frame) ### new code
    clientsocket.sendall(struct.pack("H", len(data))+data) ### new 