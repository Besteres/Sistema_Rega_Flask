from bson import json_util
import json

from flask import Flask, render_template
from flask_socketio import SocketIO

from logger import Logger


app = Flask(__name__)
app.config['SECRET_KEY'] = 'S3cr3t!'
socket = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def data_update(data):
    print(data)
    socket.emit('data_update', json.dumps(data, default=json_util.default))


if __name__ == '__main__':
    print("Imported")
    log = Logger()
    log.on_data_updated(data_update)
    app.run(host='0.0.0.0', debug=False)
