#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules
import numpy
import cv2
import os
import pickle
import scipy
import filters
import xbox
import math
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from time import sleep
import PIL


os.system('xset r off')
ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']


HOST = '192.168.43.46'    # Laure (Ionis's Down) IP address
#HOST = '172.20.10.11'     # Thibaut (iPhone) IP address
PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR)                    # Connect with the server
tcpCliSock.setblocking(1)

dira = 0

dic_dir = {-1: "left", 0: "forward", 1: "right"}
dic_dir_l = {1: "left", 0: "home", 2: "right"}

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

class Counter:
    i = 1437

def get_img():
    length = recvall(tcpCliSock, 16)
    print 'rec len'
    stringData = recvall(tcpCliSock, int(length))
    print 'rec img'
    img = numpy.fromstring(stringData, dtype='uint8')
    imgdec = cv2.imdecode(img, 1)
    return imgdec

'''
def get_image():
    img = tcpCliSock.recv()

top.bin("<<GetImg>>", get_image)
top.event_generate("<<GetImg>>", when="tail")
'''

def process_dir(dir):
    print dir
    tcpCliSock.send(dir)
    get_img(dir)

# =============================================================================
# The function is to send the command forward to the server, so as to make the
# car move forward.
# =============================================================================
def forward_fun(event):
    process_dir("forward")

def backward_fun(event):
    process_dir("backward")

def left_fun(event):
    global dira
    dira = -1
    process_dir("left")

def right_fun(event):
    global dira
    dira = 1
    process_dir("right")

def stop_fun(event):
    process_dir('stop')

def home_fun(event):
    global dira
    dira = 0
    process_dir('home')

def x_increase(event):
    process_dir('x+')

def x_decrease(event):
    process_dir('x-')

def y_increase(event):
    process_dir('y+')

def y_decrease(event):
    process_dir('y-')

def xy_home(event):
    process_dir('xy_home')

spd = 100

def changeSpeed():
    tmp = 'speed'
    global spd
    data = tmp + str(spd)  # Change the integers into strings and combine them with the string 'speed'.
    print 'sendData = %s' % data
    tcpCliSock.send(data)  # Send the speed data to the server(Raspberry Pi)


def main():
    #get_img()
    changeSpeed()

    #rep = tcpCliSock.recv(64)
    #get_img()

    #tcpCliSock.recv(64)
    joy = xbox.Joystick()
    last_trig = False
    last_x = 0
    data = ''
    while True:
        t = joy.rightTrigger()
        x = joy.rightX()
        cur_trig = t > 0
        if (not(last_trig == cur_trig)):
            last_trig = cur_trig
            if (cur_trig == 0.0):
                send_data(tcpCliSock, 'stop')
            if (cur_trig > 0):
                send_data(tcpCliSock, 'forward')
        if (not(x == last_x)):
            if (x == 0):
                #send_data(tcpCliSock, 'home')
                send_data(tcpCliSock, 'home')
            last_x = x
            angle = int(x * 180 + 180)
            if (angle == 180):
                continue
            if (angle > 180):
                tmp = angle - 180
                angle = 180 + int(tmp * 0.8)
            if (angle < 180):
                angle = 180 - int((180 - angle) * 0.8)
            if (angle > 225):
                angle = 225
            #if (x > 0):
                #send_data(tcpCliSock, 'right')
            #    send_data(tcpCliSock, 'turn=360')
            #if (x < 0):
                #send_data(tcpCliSock, 'left')
            #    send_data(tcpCliSock, 'turn=0')
            data = 'turn=' + str(angle)
            send_data(tcpCliSock, data)

def send_data(tcpCliSock, data):
    print data
    tcpCliSock.send(data)
    #tcpCliSock.recv(64)
    sleep(0.2)

if __name__ == '__main__':
	main()
