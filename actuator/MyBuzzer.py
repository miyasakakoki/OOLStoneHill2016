#!/usr/bin/python

import time
from grovepi import *
import math
from socket import *
import threading


buzzer_pin = 2		#Port for buzzer
led_pin = 4         #Port for led

host = ''
port = 4000

buzzer = False
buzzerth = True

def hoge():
    while buzzerth:
        time.sleep(0.5)
        if buzzer:
            digitalWrite( buzzer_pin, 1 )
            time.sleep(0.5)
            digitalWrite( buzzer_pin, 0 )


thre = threading.Thread(target=hoge, name="thre")
thre.start()

pinMode(buzzer_pin,"OUTPUT")	# Assign mode for buzzer as output
pinMode(led_pin,"OUTPUT")		# Assign mode for led as output
time.sleep(1)

s = socket( AF_INET, SOCK_DGRAM )
s.bind((host,port))

while True:
    try:
        mes,address = s.recvfrom(4096)
        if "Buzzer" in mes:
            if "on" in mes:
                buzzer = True
            elif "off" in mes:
                buzzer = False
        elif "LED" in mes:
            if "on" in mes:
                digitalWrite(led_pin,1)
            elif "off" in mes:
                digitalWrite(led_pin,0)
        digitalWrite(buzzer_pin,1)
        digitalWrite(buzzer_pin,0)
    except KeyboardInterrupt:	# Stop the buzzer before stopping
        buzzerth = False
        thre.stop()
        digitalWrite(buzzer_pin,0)
        break
    except (IOError,TypeError) as e:
        print("Error")

