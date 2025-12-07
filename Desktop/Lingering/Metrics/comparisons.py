import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

class MetricsVisualiser:
    def __init__(self):
        """ Instantiate attributes
        
        Attributes:
        - Methods (hashmap[str][str]): All implementations and full names
        - Scenarios (list[str]): Name of all situations tested on
        - OutputDirectory (str): Where PNGs are saved

        Returns:
        - None
        """
        self.Methods = {
            "BLOB": "Binary Large Object",
            "HS": "Human Segmentation",
            "PE": "Pose Estimation"
        }

        self.Scenarios = ["Behind", "Hiding", "Moving", "Object", "Standing"]
        self.OutputDirectory = "Plots"
        os.makedirs(self.OutputDirectory, exist_ok=True)

    def LoadCSV(self, Method, Scenario):
        """ Returns recorded CSV as a dataframe
        
        Arguments:
        - Method (str): Name of implementation experimented
        - Scenario (str): Situation implementation was tested in

        Returns:
        - pd.DataFrame: Data from CSV file
        """
        FileName = f"{Method} - {Scenario}.csv"
        return pd.read_csv(FileName)

    def StatusToNumeric(self, Status):
        """ Convert the status of monitor to a numeric value
        
        Arguments:
        - Status (str): Status from the current frame

        Returns:
        - int: 0 if persons present, 1 if persons lingering
        """
        if isinstance(Status, str):
            Status = Status.lower()
            if "present" in Status:
                return 0
            if "linger" in Status:
                return 1
        return np.nan

    def ExpectedLine(self, Scenario, Frames):
        """ Generates array representing what performance is expected

        Arguments:
        - Scenario (str): Name of the scenario displayed
        - Frames (int): Number of frames record

        Returns:
        - Expected (np.ndarray): Array with values of whats expected or not
        """
        Expected = np.zeros(Frames)

        if Scenario in ["Behind", "Hiding", "Standing"]:
            Expected[10:10 + 50] = 1
        return Expected

    def PlotScenario(self, DF, Scenario, Ax):
        """ Plots method performance for a given scenario

        Arguments:
        - DF (pd.DataFrame): CSV data for a given scenario
        - Scenario (str): Name of scenario plotted
        - Ax (matplotlib.axes.Axes): Axis to draw plot on
        
        Returns:
        - None
        """
        DF["StatusNumeric"] = DF["Status"].apply(self.StatusToNumeric)

        Frames = len(DF)
        Seconds = DF["FrameNumber"] 

        if Scenario in ["Behind", "Hiding", "Standing"]:
            Expected = self.ExpectedLine(Scenario, Frames)
            Ax.plot(Seconds, Expected + 0.05, linestyle="--", linewidth=2, color="#AA00FF", alpha=0.6, label="Expected")

        Ax.plot(Seconds, DF["StatusNumeric"], linewidth=2, alpha=0.9, label="Achieved", color="tab:blue")

        NoPersonMask = DF["Status"].str.lower().str.contains("no", na=False)
        for i in np.where(NoPersonMask)[0]:
            Time = Seconds.iloc[i]
            Ax.axvspan(Time - 0.5, Time + 0.5, color="red", alpha=0.12)

        PresentMask = DF["PersonDetected"] == 1
        if PresentMask.any():
            Segments = np.where(PresentMask)[0]
            Start = Segments[0]
            for i in range(1, len(Segments)):
                if Segments[i] != Segments[i - 1] + 1:
                    Ax.hlines(-0.2, DF["FrameNumber"].iloc[Start], DF["FrameNumber"].iloc[Segments[i - 1]], linewidth=5, color="black") 
                    Start = Segments[i]
            Ax.hlines(-0.2, DF["FrameNumber"].iloc[Start], DF["FrameNumber"].iloc[Segments[-1]], linewidth=5, color="black")

        Ax.set_title(Scenario, fontsize=13, weight="bold")
        Ax.set_ylabel("Status")
        Ax.set_yticks([0, 1])
        Ax.set_yticklabels(["Present (0)", "Lingering (1)"])
        Ax.grid(True, linestyle="--", alpha=0.4)
        Ax.legend(loc="upper right", fontsize=8)

    def PlotMethod(self, Method):
        """ Plot all methods and their performance against each scenarios

        Arguments:
        - Method (str): Name of implementation

        Returns:
        - None
        """
        Figure, Axes = plt.subplots(5, 1, figsize=(14, 14))
        Figure.suptitle(f"{self.Methods[Method]} – Lingering Behaviour", fontsize=18, weight="bold")

        for i, Scenario in enumerate(self.Scenarios):
            DF = self.LoadCSV(Method, Scenario)
            self.PlotScenario(DF, Scenario, Axes[i])
            Axes[i].set_xlabel("Time (seconds)")

        plt.tight_layout(rect=[0, 0, 1, 0.97])
        Results = os.path.join(self.OutputDirectory, f"{Method}_ALL.png")
        plt.savefig(Results)
        plt.close()

    def Generate(self):
        """ Retrieve all methods and their performances

        Returns:
        - None
        """
        for Method in self.Methods:
            self.PlotMethod(Method)

if __name__ == "__main__":
    # Visualise all methods against all scenarios
    LingeringVisualiser = MetricsVisualiser()
    LingeringVisualiser.Generate()