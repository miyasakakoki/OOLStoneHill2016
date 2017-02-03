#!/usr/bin/python

from flask import Flask,request,redirect
import os
app = Flask(__name__)

device = [
#    { "MAC":"b8:27:eb:33:95:f9" }, #dev1 sw
    { "MAC":"5c:cf:7f:89:f3:b0" },
    { "MAC":"18:fe:34:d2:83:40" }, #dev2 led
    { "MAC":"18:fe:34:d2:7b:29" } #dev3 buzzer
]

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/api/con", methods=["POST"])
def connect():
    dev1mac= device[int(request.form['devid'])-1]["MAC"]
    dev2mac= device[int(request.form['conect'])-1]["MAC"]
    command = 'curl -X POST -d \'{"mac1":"' + dev1mac + '","mac2":"' + dev2mac + '"}\' http://localhost:8080/api/sr'
    os.system( command );
    return redirect("/")



if __name__ == "__main__":
    app.run( host='0.0.0.0', port=80)


# curl -X POST -d '{"mac1":"02:00:00:00:00:01","mac2":"02:00:00:00:00:02"}' http://localhost:8080/api/sr 

