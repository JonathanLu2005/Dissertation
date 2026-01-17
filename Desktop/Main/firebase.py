import time 
import firebase_admin 
from firebase_admin import credentials, db 
import os 
from dotenv import load_dotenv 
from pathlib import Path
from Desktop.Main.main import Main
import winsound

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
    AlertReference = db.reference("AlertSettings/Laptop")
    AppReference = db.reference("AppMessages")

    while True:
        for Result in Main():
            AlertSettings = AlertReference.get() or {}
            AlertsEnabled = AlertSettings.get("enabled", True)
            AlertsVolume = float(AlertSettings.get("volume", 1.0))
            Message = "No suspicious activity detected"

            if Result and AlertsEnabled:
                winsound.Beep(1500, int(500 * AlertsVolume))
                Message = "Suspicious activity detected"

            BackendReference.set({
                "Alert": Result,
                "Message": Message
            })

            print("Sent to App")
        time.sleep(3)

Firebase()