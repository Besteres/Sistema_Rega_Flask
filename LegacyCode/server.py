from flask import Flask
from .routes import main
from .events import socketio





#socketio = SocketIO(app)

#sistema = Sistema(key="aVAOSP2Gr2MuGkv1aq7tvirf0Cj1Qe4T",citykey="272831",timesremain=50)
def create_Server():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'LP_Trabalho'
    app.register_blueprint(main)
    socketio.init_app(app)
    return app

'''
@socketio.event
def getValues():
    global sistema
    return jsonify({"Temperatura":sistema.getValues()[0],"Humidade":sistema.getValues()[1]})
'''

'''
@app.route("/uploadvalues",methods=["POST"])
def uploadValues():
    conn = db_connection()
    cur = conn.cursor()
    j_body = request.get_json()
'''



'''
if __name__ == '__main__':
    socketio.run(app,host="192.168.1.186",port=443,debug=True)

'''