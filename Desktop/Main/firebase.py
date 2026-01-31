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
    AppReference = db.reference("AppMessages")
    LocationReference = db.reference("LaptopLocation")
    ControlPanel = db.reference("RemoteControl")

    ImagePath = os.path.join(BaseDirectory, "Warning.png")
    Warning = cv2.imread(ImagePath)
    cv2.imshow("Warning", Warning)
    cv2.waitKey(1)

    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

    while True:
        ControlPanelResults = ControlPanel.get() or {}
        PowerOn = ControlPanelResults.get("Power", False)
        LockOn = ControlPanelResults.get("Lock", False)
        CameraOn = ControlPanelResults.get("Camera", False)

        AlertSettings = AlertReference.get() or {}
        AlertsEnabled = AlertSettings.get("enabled", True)
        AlertsVolume = float(AlertSettings.get("volume", 1.0))

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
            for Result in Main():
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