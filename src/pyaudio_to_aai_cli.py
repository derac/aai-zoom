"""Get audio from compute with pyaudio, send to AssemblyAI API and display transcription in STDOUT"""

import argparse

import pyaudio
import websockets
import asyncio
import base64
import json

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

audio = pyaudio.PyAudio()
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER,
)

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


async def send_receive():
    print(f"Connecting websocket to url ${URL}")
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", args.auth_key),),
        ping_interval=5,
        ping_timeout=20,
    ) as web_socket:
        await asyncio.sleep(0.1)
        session_begins = await web_socket.recv()
        print(session_begins)

        async def send():
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    await web_socket.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                await asyncio.sleep(0.01)
            return True

        async def receive():
            while True:
                try:
                    result_str = await web_socket.recv()
                    json_result = json.loads(result_str)
                    if "text" in json_result:
                        print(json_result["text"])
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        await asyncio.gather(send(), receive())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-auth_key", "-k", type=str, required=True)
    args = parser.parse_args()

    asyncio.run(send_receive())
