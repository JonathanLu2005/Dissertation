import time 
from Desktop.Main.main import Main
import winsound
import ctypes
import asyncio
from Desktop.Main.livestream import Streamer, StartStreamingServer, StreamLoop
from Desktop.Main.mic import StartAudioStream
import threading
from Desktop.Main.camera import CameraManager
from Desktop.Main.location import GetLocation
from Desktop.Main.generateMonitors import GenerateMonitors
from Desktop.Main.generateReferences import GenerateFirebase, RetrieveControlPanel, RetrieveAlerts, RetrieveLocks, RetrieveModels
from Desktop.Main.setReferences import SetIP, SetLocation, SetBackend
from Desktop.Main.cloud import UploadLog
import socket

def Firebase():
    """ Establish connection to the Firebase server

    Returns:
    - None
    """
    BackendReference, PerformanceReference, IPReference, AlertReference, LocationReference, LockingReference, ModelReference, ControlPanel = GenerateFirebase()
    StreamCurrent = False
    PreviousSuspiciousDetected = False

    LocalIP = str(socket.gethostbyname(socket.gethostname()))
    SetIP(IPReference, LocalIP)

    Monitors = GenerateMonitors()

    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
    Camera = None

    StartStreamingServer()
    StartAudioStream()

    while True:
        PowerOn, LockOn, CameraOn = RetrieveControlPanel(ControlPanel)
        AlertsEnabled, AlertsVolume = RetrieveAlerts(AlertReference)
        DetectionLock, PowerLock = RetrieveLocks(LockingReference)
        BackgroundModel, ProximityModel, LoiteringModel, MaskModel = RetrieveModels(ModelReference)

        if PowerOn and Camera is None:
            Camera = CameraManager()
            threading.Thread(
                target=StreamLoop,
                args=(Camera,),
                daemon=True
            ).start()

        if CameraOn and not StreamCurrent:
            Streamer.On = True
            StreamCurrent = True 

        if not CameraOn and StreamCurrent:
            Streamer.On = False
            StreamCurrent = False

        if not PowerOn and Camera is not None:
            Camera.Release()
            Camera = None

        SuspiciousDetected = False
        Message = "Powered off"

        Latitude, Longitude = asyncio.run(GetLocation())
        SetLocation(LocationReference, Latitude, Longitude)

        if LockOn:
            ctypes.windll.user32.LockWorkStation()

        CurrentTime = int(time.time())

        if PowerOn:
            if PowerLock:
                ctypes.windll.user32.LockWorkStation()

            Frame = Camera.GetFrame()
            SuspiciousDetected, Message = Main(BackgroundModel, ProximityModel, LoiteringModel, MaskModel, Frame, Monitors)

            if SuspiciousDetected:
                if DetectionLock:
                    ctypes.windll.user32.LockWorkStation()

                if AlertsEnabled:
                    winsound.Beep(1500, int(500 * AlertsVolume))

                if not PreviousSuspiciousDetected:
                    ImageName = str(CurrentTime) + ".jpg"
                    UploadLog(Frame, ImageName, Message)
            PreviousSuspiciousDetected = SuspiciousDetected
            

        SetBackend(BackendReference, SuspiciousDetected, Message, CurrentTime)
        print("Sent:", Message)
        time.sleep(1)

Firebase()