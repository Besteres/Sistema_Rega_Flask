from .extensions import socketio
from flask_socketio import emit
from .Sistema import Sistema
sistema = Sistema(key="aVAOSP2Gr2MuGkv1aq7tvirf0Cj1Qe4T",citykey="currentcityKey.txt",timesremain=50,HumidityMin=15,HumidityMax=45)

@socketio.on("connect")
def handle_connect():
    print("Client Connected")


@socketio.on("getAllValues")
def getValues():
    emit("Values",sistema.getValues())
    emit("CityValues",sistema.getCityValues())
    emit("RuleValues",sistema.getRuleValues())


@socketio.on("ChangeCidade")
def changeCidade(data):
    emit("CidadeMudada",sistema.mudarCidade(data))

@socketio.on("UpdateCidade")
def updateCidade():
    emit("CityValues",sistema.getCityValues())