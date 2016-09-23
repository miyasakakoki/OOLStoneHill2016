#!/usr/bin/python

from __future__ import print_function
from grovepi import *
import socket
from contextlib import closing

dht_sensor_port = 7
host = '10.0.0.100'
#host = '192.168.52.100'
port = 4000
bufsize = 4096

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
with closing( sock ):
    while True:
        try:
            [ temp,hum ] = dht( dht_sensor_port, 0 )
            mes = "[ { \"Type\":\"Templature\", \"Value\":\""+str(temp)+"\" }, { \"Type\":\"Humidity\", \"Value\":\""+str(hum)+"\" } ]"
            print(mes) #debug printing
            sock.sendto( mes.encode('utf-8'),(host,port) )
            time.sleep(1)
        except (IOError,TypeError) as e:
            print("Error")
