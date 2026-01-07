import time 
import firebase_admin 
from firebase_admin import credentials, db 
import os 
from dotenv import load_dotenv 
from pathlib import Path
from Desktop.Main.main import main

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
    AppReference = db.reference("AppMessages")

    while True:
        for Result in main():
            if Result:
                BackendReference.set("Suspicious activity detected")
                print("Sent to App")
            else:
                BackendReference.set("No suspicious activity detected")
                print("Sent to App")

        #Message = AppReference.get()
        #print(f"{Message} from App")

        time.sleep(3)

Firebase()