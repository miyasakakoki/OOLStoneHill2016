#!/usr/bin/python

from grovepi import *


sensor_port = 7

while True:
	try:
		[ tmp, hum ] = dht( sensor_port, 1 )
		print "
