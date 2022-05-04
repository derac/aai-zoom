# Install

1. install ubuntu 20.04
1. set resolution to 1680x1050, add it to grub if necessary
   - I did this like so with hyper-v https://superuser.com/questions/518484/how-can-i-increase-the-hyper-v-display-resolution
1. `sudo apt update`
1. `sudo apt-get install portaudio19-dev python3-pyaudio redis`
1. `pip install -r requirements.txt`
1. install zoom https://zoom.us/download
   - set browser to always use zoommtg for zoom links
   - set zoom to remember name and turn off cam on first open
1. `python3 ./src/flask_server_example.py -k AAI_API_KEY`

# Implementation notes

- [./src/flask_server_example.py](./src/flask_server_example.py) is used to start the Flask and socketio server. It is hosted at [127.0.0.1:8000](127.0.0.1:8000).
- [./src/open_zoom_meeting.py](./src/open_zoom_meeting.py) is used to control opening the links sent through the /transcription endpoint.
- [./src/pyaudio_to_aai_flask.py](./src/pyaudio_to_aai_flask.py) is used to pipe audio from the computer (default speaker) to socketio through the redis queue.
- There is some code in the Flask server file to manage these last two as subprocesses.
- [./src/static/zoom-transcribe.js](./src/static/zoom-transcribe.js) contains the client side code for interacting with the socketio server and displaying the translation.
