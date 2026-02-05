import asyncio
import websockets 
import pyaudio 
import threading

Format = pyaudio.paInt16 
Channels = 1 
Rate = 16000
Chunk = 512

Audio = pyaudio.PyAudio()
Stream = Audio.open(
    format=Format,
    channels=Channels,
    rate=Rate,
    output=True,
    frames_per_buffer=Chunk
)

async def AudioHandler(LiveAudio):
    """ Receive live audio and plays it

    Arguments:
    - LiveAudio (audio chunks): Audio received from app

    Returns:
    - None
    """
    async for Data in LiveAudio:
        Stream.write(Data)

async def RunAudioServer():
    """ Starts websocket server to receive audio

    Returns:
    - None
    """
    async with websockets.serve(AudioHandler, "0.0.0.0", 8765):
        await asyncio.Future()

def StartAudioStream():
    """ Launches audio server with thread

    Returns:
    - None
    """
    threading.Thread(
        target=lambda: asyncio.run(RunAudioServer()),
        daemon=True
    ).start()