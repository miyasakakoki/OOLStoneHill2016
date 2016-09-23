#!/usr/bin/python

import json
import socket
from contextlib import closing
import time

rs = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

#host = ('192.168.0.1',4000)
host = ('10.0.0.101', 4000 )


with closing( rs ):
	rs.bind( ('10.0.0.1', 4000) )
	while True:
		mes,addr = rs.recvfrom( 4096 )
		if len(mes) != 82:
			continue
		j = json.loads(mes)
		hum = temp = -256
		for x in j:
			if x["Type"] == "Templature":
				temp = float(x["Value"])
			elif x["Type"] == "Humidity":
				hum = float(x["Value"])
		if temp != -256 and hum != -256:
			hukai = 0.81*temp+0.01*hum*(0.99*temp-14.3)+46.3
			print( hukai )
			hukai = (hukai >= 75)
			ss = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
			with closing(ss):
				ss.sendto( ("{\"Buzzer\":\""+("on" if hukai else "off")+"\"}").encode('utf-8'), host )
				ss.sendto( ("{\"LED\":\""+("off" if hukai else "on")+"\"}").encode('utf-8'), host )




