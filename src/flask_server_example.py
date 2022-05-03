import asyncio, subprocess, os
from multiprocessing import Process

from flask import Flask, render_template, request
from flask_socketio import SocketIO

from open_zoom_meeting import open_zoom_meeting
from pyaudio_to_aai_flask import send_receive

PYAUDIO_AAI_PROCESS = None

app = Flask(__name__)
socketio = SocketIO(app, message_queue="redis://")


@socketio.on("connect")
def connect():
    print("client connected")
    socketio.emit("connect", "")


@socketio.on("disconnect")
def disconnect():
    global PYAUDIO_AAI_PROCESS
    print("client disconnected")
    if PYAUDIO_AAI_PROCESS:
        if PYAUDIO_AAI_PROCESS.is_alive():
            PYAUDIO_AAI_PROCESS.kill()
            PYAUDIO_AAI_PROCESS = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transcribe", methods=["POST"])
def transcribe():
    global PYAUDIO_AAI_PROCESS
    meeting_url = request.get_data(as_text=True)
    print(f"joining {meeting_url}")
    # open zoom meeting
    subprocess.Popen(
        [
            "python3",
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "open_zoom_meeting.py"
            ),
            "-meeting_url",
            meeting_url,
        ]
    )
    # make sure aai api process is listening
    if not PYAUDIO_AAI_PROCESS:
        PYAUDIO_AAI_PROCESS = Process(
            target=asyncio.run, args=(send_receive(args.auth_key),)
        )
        PYAUDIO_AAI_PROCESS.start()
    return "running transcription"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-auth_key", "-k", type=str, required=True)
    args = parser.parse_args()

    socketio.run(app, port=8000)
