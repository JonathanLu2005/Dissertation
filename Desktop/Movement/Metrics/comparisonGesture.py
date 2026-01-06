import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

class MetricsVisualiser:
    def __init__(self):
        """ Initialise file names and implementations to retrieve data and plot graphs
        
        Returns:
        - None
        """
        self.FileNames = {
            "DD": "Hands - DD.csv",
            "PD": "Hands - PD.csv",
            "TD": "Hands - TD.csv"
        }

        self.Methods = {
            "DD": "Distance and Depth",
            "PD": "Proximity Distance",
            "TD": "Trajectory and Distance"
        }

        self.OutputDirectory = "Plots"
        os.makedirs(self.OutputDirectory, exist_ok=True)

    def LoadCSV(self, FilePath):
        """ Retrieves dataframe

        Arguments:
        - FilePath (str): Path to CSV file

        Returns:
        - pd.DataFrame: CSV contents
        """
        return pd.read_csv(FilePath)

    def StatusToNumeric(self, Status):
        """ Convert arguments to 0 or 1 to visualise
        
        Arguments:
        - Status (str): Status from frame processed

        Returns:
        - float: Placeholder nan value for method to apply on CSV
        """
        if not isinstance(Status, str):
            return float("nan")

        Status = Status.strip().upper()
        if Status == "NO_REACH":
            return 0
        if Status == "REACHING":
            return 1

        return float("nan")

    def PlotMethod(self, Method):
        """ Given implementation, plot their performance
        
        Arguments:
        - Method (str): Implementation name

        Returns:
        - None
        """
        MethodCSV = self.FileNames[Method]
        DF = self.LoadCSV(MethodCSV)
        if DF is None:
            return

        GraphTitle = self.Methods[Method]
        DF["StatusToNumeric"] = DF["Status"].apply(self.StatusToNumeric)
        Frames = len(DF)
        
        if Frames >= 200: 
            Half = 100 
        else: 
            Half = Frames // 2

        Expected = np.zeros(Frames)
        Expected[:Half] = 1
        ExpectedPlot = Expected + 0.05

        plt.figure(figsize=(14, 6))
        plt.title(f"{GraphTitle} – Gesture Detection Output", fontsize=16, weight="bold")
        plt.plot(DF["FrameNumber"], DF["StatusToNumeric"], label="Achieved", linewidth=2.2, color="tab:blue")
        plt.plot(DF["FrameNumber"], ExpectedPlot, label="Expected", linewidth=2.4, linestyle="--", color="#AA00FF", alpha=0.8)
        plt.xlabel("Frame Number")
        plt.ylabel("Value")
        plt.yticks([0, 1], ["NO_REACH (0)", "REACHING (1)"])
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        FileName = os.path.join(self.OutputDirectory, f"Gesture {Method}.png")
        plt.savefig(FileName)
        plt.close()

    def GeneratePlots(self):
        """ Traverse all implementations and plot their performance

        Returns:
        - None
        """
        for Method in self.FileNames.keys():
            self.PlotMethod(Method)

if __name__ == "__main__":
    GestureVisualiser = MetricsVisualiser()
    GestureVisualiser.GeneratePlots()