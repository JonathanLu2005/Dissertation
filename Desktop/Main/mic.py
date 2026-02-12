import asyncio
import websockets 
import pyaudio 
import threading

Format = pyaudio.paInt16 
Channels = 1 
Rate = 16000
Chunk = 2048

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
    try:
        async for Data in LiveAudio:
            if len(Data) > Chunk * 2:
                Data = Data[-Chunk * 2:]  
            Stream.write(Data)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

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