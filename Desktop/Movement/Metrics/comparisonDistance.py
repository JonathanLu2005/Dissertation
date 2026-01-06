import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

class MetricsVisualiser:
    def __init__(self):
        """ Initiates the methods and scenarios to plot and where to store
        
        Attributes:
        - Methods (dict): Different implementations
        - Scenarios (list): Different scenarios
        - OutputDirectory (str): Folder to store graphs

        Returns:
        - None
        """
        self.Methods = {
            "BPP": "Bounding Box",
            "FDE": "Face Distance Estimation",
            "Hybrid": "Hybrid",
            "PD": "Pose Distance"
        }

        self.Scenarios = ["Standing", "Sitting", "Crouch"]
        self.OutputDirectory = "Plots"
        os.makedirs(self.OutputDirectory, exist_ok=True)

    def LoadCSV(self, Method, Scenario):
        """ Load CSV for specific implementation and scenario

        Arguments:
        - Method (str): Name of implementation
        - Scenario (str): Name of situation

        Returns:
        - pd.DataFrame: CSV contents
        """
        FileName = f"{Method} - {Scenario}.csv"
        return pd.read_csv(FileName)

    def StatusToNumeric(self, Status):
        """ Converts status to 1 or 0 to signal if persons too close, to graph it
        
        Arguments:
        - Status (str): Result of the frame processed

        Returns:
        - float: Placeholder nan value to ensure it works on the dataframe
        """
        Status = Status.strip().lower()
        if "safe" in Status:
            return 0
        if "close" in Status:
            return 1

        return float("nan")

    def PlotSingleScenario(self, DF, Scenario, Ax, Index):
        """ Plot expected and achieved results from a scenario

        Arguments:
        - DF (pd.DataFrame): CSV with values from processing frame
        - Scenario (str): Name of scenario
        - Ax (matplotlib.axes.Axes): Axis to draw on
        - Index (int): Subplot position

        Returns:
        - None
        """
        if DF is None:
            Ax.set_title(f"{Scenario} (Missing Data)")
            Ax.axis("off")
            return

        DF["StatusNumeric"] = DF["Status"].apply(self.StatusToNumeric)
        Frames = len(DF)

        if Frames >= 200:
            Half = 100
        else:
            Half = Frames // 2

        Expected = np.zeros(Frames)
        Expected[:Half] = 1
        ExpectedPlot = Expected + 0.05

        Ax.plot(ExpectedPlot, linestyle="--", linewidth=2.2, alpha=0.65, color="#AA00FF", label="Expected")
        Ax.plot(DF["StatusNumeric"], linewidth=2, label="Achieved", alpha=0.9, color="tab:blue")

        MissingValues = DF["Status"].str.lower().str.contains("no", na=False)
        if MissingValues.any():
            for IndexMissing in np.where(MissingValues)[0]:
                Ax.axvspan(IndexMissing - 0.5, IndexMissing + 0.5, color="red", alpha=0.12)

        Ax.set_title(Scenario, fontsize=13, weight="bold")
        Ax.set_ylabel("Status")
        Ax.set_yticks([0, 1])
        Ax.set_yticklabels(["Safe (0)", "Too Close (1)"])
        Ax.grid(True, linestyle="--", alpha=0.4)

        if Index == 2:
            Ax.set_xlabel("Frame #")

        Ax.legend(loc="upper right", fontsize=8)

    def PlotMethodAllScenarios(self, Method):
        """ Plots the method and all scenarios and how it performed

        Arguments:
        - Method (str): Name of implementation

        Returns:
        - None
        """
        Figure, Axes = plt.subplots(3, 1, figsize=(12, 10))
        Figure.suptitle(f"{self.Methods[Method]} – Real Detection Output", fontsize=16, weight="bold")

        for i, Scenario in enumerate(self.Scenarios):
            DF = self.LoadCSV(Method, Scenario)
            Ax = Axes[i]
            self.PlotSingleScenario(DF, Scenario, Ax, i)

        plt.tight_layout([0, 0, 1, 0.96])
        FileName = os.path.join(self.OutputDirectory, f"{Method}_ALL.png")
        plt.savefig(FileName)
        plt.close()

    def GeneratePlots(self):
        """ Generate all method graphs with their scenarios

        Returns:
        - None
        """
        for Method in self.Methods.keys():
            self.PlotMethodAllScenarios(Method)

if __name__ == "__main__":
    DistanceVisualiser = MetricsVisualiser()
    DistanceVisualiser.GeneratePlots()