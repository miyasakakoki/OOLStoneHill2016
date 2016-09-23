#!/usr/bin/python

from flask import Flask,request,redirect
import os
app = Flask(__name__)

device = [
    { "MAC":"b8:27:eb:01:67:24" }, #dev1
    { "MAC":"b8:27:eb:35:02:c9" }, #dev2
    { "MAC":"b8:27:eb:c5:ba:92" } #dev3
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

