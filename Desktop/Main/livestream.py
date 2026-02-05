import cv2
import time 
from fastapi import FastAPI 
from fastapi.responses import StreamingResponse 
import uvicorn
import threading

class LiveStream:
    def __init__(self):
        """ Ensure frames are streamed without them being overwritten

        Attributes:
        - Frame (np.ndarray): Current frame
        - On (bool): Determine if live stream is on or not
        - Lock (thread.lock): Threading lock to avoid overwriting frames sent to live stream

        Returns:
        - None
        """
        self.Frame = None 
        self.On = False
        self.Lock = threading.Lock()

    def Update(self, Frame):
        """ Uses the lock to update the frame to stream
        
        Arguments:
        - Frame (np.ndarray): Current frame shown

        Returns:
        - None
        """
        with self.Lock:
            self.Frame = Frame.copy()

    def Frames(self):
        """ Streams the current frame if there is one via the locking mechanism

        Returns:
        - None
        """
        while True:
            if not self.On:
                time.sleep(0.1)
                continue 

            with self.Lock:
                if self.Frame is None:
                    Frame = None
                else:
                    Frame = self.Frame.copy()

            if Frame is None:
                time.sleep(0.1)
                continue 

            Success, Buffer = cv2.imencode(".jpg", Frame)
            if not Success:
                continue 

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                Buffer.tobytes() + b"\r\n"
            )

App = FastAPI()
Streamer = LiveStream()

@App.get("/Stream")
def Stream():
    """ Streams the frames to a local HTTP server

    Returns:
    - None
    """
    return StreamingResponse(
        Streamer.Frames(),
        media_type = "multipart/x-mixed-replace; boundary=frame"
    )

def StartStreamingServer():
    """ Enable threading to stream the video

    Returns:
    - None
    """
    threading.Thread(
        target = lambda: uvicorn.run(App, host="0.0.0.0", port=8000, log_level="warning"),
        daemon=True
    ).start()