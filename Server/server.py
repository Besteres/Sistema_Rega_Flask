from flask import Flask, send_from_directory, request, render_template, session, copy_current_request_context

from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config['SECRET_KEY'] = 'LP_Trabalho'
socketio = SocketIO(app)

@app.route("/",methods=["GET"])
def home():
    return render_template("home.html")


if __name__ == '__main__':
    socketio.run(app,host="192.168.1.75",port=443,debug=True)