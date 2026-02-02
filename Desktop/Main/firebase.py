import time 
import firebase_admin 
from firebase_admin import credentials, db, storage
import os 
from dotenv import load_dotenv 
from pathlib import Path
from Desktop.Main.main import Main
import winsound
import cv2
import ctypes
import asyncio
from winrt.windows.devices.geolocation import Geolocator 

class CameraManager:
    def __init__(self):
        """ Retrieve frames from camera to analyse

        Attributes:
        - Cap (cv2.VideoCapture): Camera
        - Frame (np.ndarray): Current frame

        Raises:
        - RuntimeError: Camera not accessible

        Returns:
        - None
        """
        self.Cap = cv2.VideoCapture(0)
        if not self.Cap.isOpened():
            raise RuntimeError("Can't access camera")
        self.Frame = None 
    
    def GetFrame(self):
        """ Return current frame

        Returns:
        - Frame (np.ndarray): Current frame
        """
        Ret, Frame = self.Cap.read()
        if not Ret:
            return None 
        self.Frame = cv2.resize(Frame, (900, 700))
        return self.Frame
    
    def Release(self):
        """ Turns off camera

        Returns:
        - None
        """
        self.Cap.release()

async def GetLocation():
    """ Retrieve laptop longitude and latitude coordinates

    Returns:
    - (float): Latitude value
    - (float): Longitude value
    """
    Location = Geolocator()
    Location.desired_accuracy_in_meters = 50
    Position = await Location.get_geoposition_async()
    Coordinates = Position.coordinate.point.position 
    return Coordinates.latitude, Coordinates.longitude

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
    firebase_admin.initialize_app(Credentials, {"databaseURL": f"https://{FirebaseID}-default-rtdb.europe-west1.firebasedatabase.app", 
                                                "storageBucket": f"https://{FirebaseID}.appspot.com"})
    FirebaseBucket = storage.bucket()
    BackendReference = db.reference("BackendMessages")
    AlertReference = db.reference("AlertSettings/Laptop")
    LocationReference = db.reference("LaptopLocation")
    ModelReference = db.reference("ModelSettings")
    ControlPanel = db.reference("RemoteControl")

    ImagePath = os.path.join(BaseDirectory, "Warning.png")
    Warning = cv2.imread(ImagePath)
    cv2.imshow("Warning", Warning)
    cv2.waitKey(1)

    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
    Camera = None

    while True:
        ControlPanelResults = ControlPanel.get() or {}
        PowerOn = ControlPanelResults.get("power", False)
        LockOn = ControlPanelResults.get("lock", False)
        CameraOn = ControlPanelResults.get("camera", False)

        AlertSettings = AlertReference.get() or {}
        AlertsEnabled = AlertSettings.get("enabled", True)
        AlertsVolume = float(AlertSettings.get("volume", 1.0))

        if PowerOn and Camera is None:
            Camera = CameraManager()

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
            Frame = Camera.GetFrame()
            for Result in Main(BackgroundModel, ProximityModel, LoiteringModel, MaskModel, Frame):
                SuspiciousDetected, Message = Result
                break 

            if SuspiciousDetected:
                if AlertsEnabled:
                    winsound.Beep(1500, int(500 * AlertsVolume))

        BackendReference.set({
            "alert": SuspiciousDetected,
            "message": Message,
            "timestamp": int(time.time())
        })

        print("Sent:", Message)
        time.sleep(3)


Firebase()