from flask import Flask, jsonify, request, abort
import psycopg2
from Client.sensor import Sensor
from time import sleep

app = Flask(__name__)
app.debug = True

sensor = Sensor()









if __name__ == "__main__":
    app.run(host='192.168.1.75', port=5000)