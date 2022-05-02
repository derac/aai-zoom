from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
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


@app.route("/transcribe", methods=["POST"])
def transcribe():
    print(request.get_data(as_text=True))
    return "blah"


if __name__ == "__main__":
    socketio.run(app, port=80)

    while True:
        emit("message", "blah")
