import csv
import os

LogFile = os.path.join(os.path.dirname(__file__), "MaskLog.csv")
if not os.path.exists(LogFile):
    with open(LogFile, "w", newline="") as File:
        writer = csv.writer(File)
        writer.writerow(["FrameNumber", "Status", "Confidence"])

def LogMask(FrameNumber, Status, Confidence):
    """ Stores metrics from evaluating mask detection implementations

    Arguments:
    - FrameNumber (int): Current frame number
    - Status (str): Status of current frame
    - Confidence (float): Confidence in mask detected or not, aside for occlusion which is percentage of face occluded
    
    Returns:
    - None
    """
    with open(LogFile, "a", newline="") as File:
        writer = csv.writer(File)
        writer.writerow([FrameNumber, Status, round(Confidence, 2)])