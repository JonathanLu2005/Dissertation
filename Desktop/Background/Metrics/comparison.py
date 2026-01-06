import pandas as pd
import matplotlib.pyplot as plt
import os

class MetricsVisualiser:
    def __init__(self):
        """ Visualises metrics from experiments to determine best method
        
        Attributes:
        - Methods (list[str]): Different methods tested
        - Scenarios (list[str]): Scenarios tested against methods
        - Metrics (list[str]): Metrics to evaluate methods

        Returns:
        - None
        """
        self.Methods = ["KNN", "MOG2", "FLOW", "Hybrid"]
        self.Scenarios = ["Normal", "Movement", "Background", "Lighting"]
        self.Metrics = ["Motion", "SSIM", "Brightness"]
        self.OutputDir = "Plots"
        os.makedirs(self.OutputDir, exist_ok=True)
        self.Data = {}
        self.LoadData()

    def LoadData(self):
        """ Retrieves metric logs
        
        Returns:
        - None
        """
        for Method in self.Methods:
            for Scenario in self.Scenarios:
                FileName = f"{Method} - {Scenario}.csv"
                if os.path.exists(FileName):
                    DF = pd.read_csv(FileName).head(200)
                    self.Data[(Method, Scenario)] = DF
                else:
                    print(f"⚠️ Missing file: {FileName}")

    def Plot(self, PrimaryList, SecondaryList, PrimaryLabel, SecondaryLabel, FileSuffix):
        """ Given metrics from method and scenarios, visualise how each method/Scenario performed

        Arguments:
        - PrimaryList (list[str]): Define each figure
        - SecondaryList (list[str]): Compared against each figure
        - PrimaryLabel (str): Name for main figures
        - SecondaryLabel (str): Name for figures comparing to
        - FileSuffix (str): To name PNG
        
        Returns:
        - None
        """
        for PrimaryItem in PrimaryList:
            Figure, Axes = plt.subplots(3, 1, figsize=(10, 10))
            Figure.suptitle(f"{PrimaryItem} {PrimaryLabel} – {SecondaryLabel}s Comparison", fontsize=16)

            for i, Metric in enumerate(self.Metrics):
                Ax = Axes[i]
                for SecondaryItem in SecondaryList:
                    if PrimaryLabel == "Scenario":
                        Key = (SecondaryItem, PrimaryItem)
                    else:
                        Key = (PrimaryItem, SecondaryItem)

                    DF = self.Data.get(Key)
                    if DF is not None and Metric in DF.columns:
                        Ax.plot(
                            range(len(DF)),
                            DF[Metric].rolling(5).mean(),
                            label=SecondaryItem,
                            linewidth=1.8,
                            alpha=0.85,
                        )

                Ax.set_title(Metric.capitalize(), fontsize=12)
                Ax.set_xlabel("Frame #")
                Ax.set_ylabel(Metric.capitalize())
                Ax.grid(True, linestyle="--", alpha=0.4)
                Ax.legend(fontsize=8)
                Ax.set_xlim(0, 200)
                Ax.set_xticks([0, 100, 200])

            plt.tight_layout(rect=[0, 0, 1, 0.96])
            Path = os.path.join(self.OutputDir, f"{PrimaryItem}{FileSuffix}.png")
            plt.savefig(Path)
            plt.close(Figure)

if __name__ == "__main__":
    Plotter = MetricsVisualiser()

    # Compare each Method against each Scenario
    Plotter.Plot(Plotter.Scenarios, Plotter.Methods, "Scenario", "Method", "_methods")

    # Compare each Scenario against each Method
    Plotter.Plot(Plotter.Methods, Plotter.Scenarios, "Method", "Scenario", "_scenarios")
