import csv
import os

LogFile = os.path.join(os.path.dirname(__file__), "ResultsLog.csv")

if not os.path.exists(LogFile):
    with open(LogFile, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Motion", "SSIM", "Brightness"])

def LogMetrics(Motion, SSIMScore, Brightness):
    """ Stores the frame Motion, SSIM, Brightness metrics into CSV
    
    Arguments:
    - Motion (float): Optical Flow measurement of motion
    - SSIMScore (float): Current frame SSIM
    - Brightness (float): Current frame brightness

    Returns:
    - None
    """

    with open(LogFile, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            round(Motion, 4),
            round(SSIMScore, 4),
            round(Brightness, 2)
        ])

