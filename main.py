from flask import Flask, jsonify, request, abort
import psycopg2

app = Flask(__name__)
app.debug = True



if __name__ == "__main__":
    app.run(host='192.168.1.75', port=5000)