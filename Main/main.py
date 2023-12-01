from bson import json_util
import json
import pred_test

from flask import Flask, render_template
from flask_socketio import SocketIO

from logger import Logger


app = Flask(__name__)
app.config['SECRET_KEY'] = 'S3cr3t!'
socket = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socket.on("ChangeCidade")
def changeCidade(data):
    log.sistema.mudarCidade(data)

@socket.on("ChangeHumidade")
def changeHumidade(data):
    min = True
    max = True
    try:
        float(data["Min"])
    except:
        print("There was no minimum given")
        min = False
    try:
        float(data["Max"])
    except:
        print("There was no max given")
        max = False


    if min or max:
        log.sistema.mudarIntervaloHumidade(data,min,max)

@socket.on("ChangePrecipitacao")
def changePrecipitacao(data):
    if(float(data)):
        log.sistema.mudarPrecipitacaoMax(data)
    
@socket.on("ChangeHistorico")
def changeHistorico(data):
    print(data)
    socket.emit('historico_update',json.dumps(pred_test.getStoredDataDay(data),default=json_util.default))

def data_update(data):
    print(data)
    socket.emit('data_update', json.dumps(data, default=json_util.default))
    


if __name__ == '__main__':
    print("Imported")
    log = Logger()
    log.on_data_updated(data_update)
    app.run(host='0.0.0.0', debug=False)
