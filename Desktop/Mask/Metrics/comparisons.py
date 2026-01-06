import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

class MetricsVisualiser:
    def __init__(self):
        """ Initiates method names and file to store method comparisons

        Attributes:
        - Methods (dict): Different implementation names
        - OutputDirectory (str): Folder to store comparisons

        Returns:
        - None
        """
        self.Methods = {
            "FOD": "Face and Object Detection",
            "OD": "Object Detection",
            "O": "Occlusion"
        }

        self.OutputDirectory = "Plots"
        os.makedirs(self.OutputDirectory, exist_ok=True)

    def LoadCSV(self, Method):
        """ Retrieve metrics for provided method

        Arguments:
        - Method (str): Name of implementation

        Returns:
        - pd.DataFrame: Implemetation metrics csv
        """
        return pd.read_csv(f"{Method} - MaskLog.csv")

    def StatusToNumeric(self, Status):
        """ Convert status to binary to signal if mask was detected or not, to plot

        Arguments:
        - Status (str): Outcome of the current frame

        Returns:
        - float: Value reflecting the status of the current frame
        """
        Status = Status.lower()

        if "no mask" in Status:
            return 0
        elif "mask detected" in Status:
            return 1
        return np.nan

    def PlotMethod(self, Method):
        """ Plot the expected and demonstrated performance for each implementation

        Arguments:
        - Method (str): Implementation name

        Returns:
        - None
        """
        DF = self.LoadCSV(Method)

        DF["StatusNumeric"] = DF["Status"].apply(self.StatusToNumeric)
        Frames = len(DF)
        Time = DF["FrameNumber"]

        Expected = np.zeros(Frames)
        Expected[60:] = 1

        plt.figure(figsize=(14, 5))
        plt.title(f"{self.Methods[Method]} – Mask Detection", fontsize=16, weight="bold")

        plt.plot(Time, Expected + 0.05, linestyle="--", linewidth=2, color="#AA00FF", alpha=0.6, label="Expected")
        plt.plot(Time, DF["StatusNumeric"], linewidth=2, color="tab:blue", alpha=0.9, label="Achieved")

        NoDetection = DF["Status"].str.lower().str.contains("no detection", na=False)
        for i in np.where(NoDetection)[0]:
            Second = Time.iloc[i]
            plt.axvspan(Second - 0.5, Second + 0.5, color="red", alpha=0.12)

        plt.yticks([0, 1], ["No Mask (0)", "Mask (1)"])
        plt.xlabel("Frame Number")
        plt.ylabel("State")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.legend(loc="upper left")

        FileName = os.path.join(self.OutputDirectory, f"{Method}_MASK.png")
        plt.tight_layout()
        plt.savefig(FileName)
        plt.close()

    def GeneratePlots(self):
        """ Plot each method and their performance 

        Returns:
        - None
        """
        for Method in self.Methods:
            self.PlotMethod(Method)

if __name__ == "__main__":
    MaskVisualiser = MetricsVisualiser()
    MaskVisualiser.GeneratePlots()
