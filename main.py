from Server.server import create_Server, socketio
app = create_Server()
socketio.run(app)
