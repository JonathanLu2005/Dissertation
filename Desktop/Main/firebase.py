import time 
import firebase_admin 
from firebase_admin import credentials, db
import os 
from dotenv import load_dotenv 
from pathlib import Path
from Desktop.Main.main import Main
import winsound
import cv2
import ctypes
import asyncio
from Desktop.Main.livestream import Streamer, StartStreamingServer, StreamLoop
from Desktop.Main.mic import StartAudioStream
import threading
from Desktop.Main.camera import CameraManager
from Desktop.Main.location import GetLocation
from Desktop.Background import background
from Desktop.Movement import distance, gesture
from Desktop.Lingering import lingering
from Desktop.Mask import mask
from Desktop.Keyboard import keyboardMonitor
from Desktop.USB import USB
from Desktop.Battery import battery
from Desktop.Trackpad import trackpad
from Desktop.Performance import performance
import socket

def Firebase():
    """ Establish connection to the Firebase server

    Returns:
    - None
    """
    BaseDirectory = os.path.dirname(__file__)
    CredentialsPath = os.path.join(BaseDirectory, "ServiceAccountKey.json")
    Credentials = credentials.Certificate(CredentialsPath)
    load_dotenv(Path(__file__).resolve().parents[2]/".env")
    FirebaseID = os.getenv("FIREBASE_PROJECT_ID")
    firebase_admin.initialize_app(Credentials, {"databaseURL": f"https://{FirebaseID}-default-rtdb.europe-west1.firebasedatabase.app"})
    BackendReference = db.reference("BackendMessages")
    PerformanceReference = db.reference("Performance")
    IPReference = db.reference("IP")
    AlertReference = db.reference("AlertSettings/Laptop")
    LocationReference = db.reference("LaptopLocation")
    LockingReference = db.reference("LockSettings")
    ModelReference = db.reference("ModelSettings")
    ControlPanel = db.reference("RemoteControl")
    StreamCurrent = False

    LocalIP = str(socket.gethostbyname(socket.gethostname()))
    IPReference.set({"ip": LocalIP})

    #ImagePath = os.path.join(BaseDirectory, "Warning.png")
    #Warning = cv2.imread(ImagePath)
    #cv2.imshow("Warning", Warning)
    #cv2.waitKey(1)

    Monitor1 = lingering.LingeringMonitor()
    Monitor2 = distance.DistanceMonitor()
    Monitor3 = mask.MaskMonitor()
    Monitor4 = background.BackgroundMonitor()
    Monitor5 = USB.USBMonitor()
    Monitor6 = battery.BatteryMonitor(10)
    Monitor7 = keyboardMonitor.KeyboardMonitor()
    Monitor8 = trackpad.TrackpadMonitor()
    Monitor9 = performance.PerformanceMonitor()
    Monitors = (Monitor1, Monitor2, Monitor3, Monitor4, Monitor5, Monitor6, Monitor7, Monitor8)

    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
    Camera = None

    StartStreamingServer()
    StartAudioStream()

    while True:
        #CPU, Memory = Monitor9.Live()
        #print(Battery)
        #print(CPU)
        #print(Memory)
        ControlPanelResults = ControlPanel.get() or {}
        PowerOn = ControlPanelResults.get("power", False)
        LockOn = ControlPanelResults.get("lock", False)
        CameraOn = ControlPanelResults.get("camera", False)

        AlertSettings = AlertReference.get() or {}
        AlertsEnabled = AlertSettings.get("enabled", True)
        AlertsVolume = float(AlertSettings.get("volume", 1.0))

        LockingSettings = LockingReference.get() or {}
        DetectionLock = LockingSettings.get("detectionlock", False)
        PowerLock = LockingSettings.get("powerlock", False)

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

        ModelSettings = ModelReference.get() or {}
        BackgroundModel = ModelSettings.get("background", True)
        ProximityModel = ModelSettings.get("proximity", True)
        LoiteringModel = ModelSettings.get("loitering", True)
        MaskModel = ModelSettings.get("mask", True)

        SuspiciousDetected = False
        Message = "Powered off"

        Latitude, Longitude = asyncio.run(GetLocation())
        Location = {
            "latitude": Latitude,
            "longitude": Longitude,
        }
        LocationReference.set(Location)

        if LockOn:
            ctypes.windll.user32.LockWorkStation()

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

        BackendReference.set({
            "alert": SuspiciousDetected,
            "message": Message,
            "timestamp": int(time.time())
        })

        print("Sent:", Message)
        time.sleep(1)

Firebase()