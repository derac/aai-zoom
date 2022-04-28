from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)


@socketio.on("connect")
def connect():
    emit("connect", "")


@socketio.on("message")
def handle_message(data):
    emit("data", data)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, port=80)

    while True:
        emit("message", "blah")
