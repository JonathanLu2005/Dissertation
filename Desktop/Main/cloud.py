from supabase import create_client 
import cv2 
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parents[2]/".env")
SupabaseURL = os.getenv("SUPABASE_URL")
SupabaseKey = os.getenv("SUPABASE_KEY")
Supabase = create_client(SupabaseURL, SupabaseKey)

def UploadLog(Frame, FileName, Message):
    """ Upload log to database

    Arguments:
    - Frame (np.ndarray): Frame when suspicious activity is detected
    - FileName (str): Name of image
    - Message (str): Message to upload

    Returns:
    - None
    """
    Success, Buffer = cv2.imencode(".jpg", Frame)
    ImageData = Buffer.tobytes()

    Supabase.storage.from_("snapshots").upload(
        FileName, 
        ImageData,
        {"content-type": "image/jpeg"}
    )

    PublicURL = Supabase.storage.from_("snapshots").get_public_url(FileName)

    Supabase.table("logs").insert({
        "message": Message,
        "image_url": PublicURL
    }).execute()