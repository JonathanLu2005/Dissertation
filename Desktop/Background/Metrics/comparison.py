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
        for method in self.Methods:
            for scenario in self.Scenarios:
                file_name = f"{method} - {scenario}.csv"
                if os.path.exists(file_name):
                    df = pd.read_csv(file_name).head(200)
                    self.Data[(method, scenario)] = df
                else:
                    print(f"⚠️ Missing file: {file_name}")

    def Plot(self, PrimaryList, SecondaryList, PrimaryLabel, SecondaryLabel, FileSuffix):
        """ Given metrics from method and scenarios, visualise how each method/scenario performed

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
            fig, axes = plt.subplots(3, 1, figsize=(10, 10))
            fig.suptitle(f"{PrimaryItem} {PrimaryLabel} – {SecondaryLabel}s Comparison", fontsize=16)

            for i, Metric in enumerate(self.Metrics):
                ax = axes[i]
                for SecondaryItem in SecondaryList:
                    if PrimaryLabel == "Scenario":
                        Key = (SecondaryItem, PrimaryItem)
                    else:
                        Key = (PrimaryItem, SecondaryItem)

                    df = self.Data.get(Key)
                    if df is not None and Metric in df.columns:
                        ax.plot(
                            range(len(df)),
                            df[Metric].rolling(5).mean(),
                            label=SecondaryItem,
                            linewidth=1.8,
                            alpha=0.85,
                        )

                ax.set_title(Metric.capitalize(), fontsize=12)
                ax.set_xlabel("Frame #")
                ax.set_ylabel(Metric.capitalize())
                ax.grid(True, linestyle="--", alpha=0.4)
                ax.legend(fontsize=8)
                ax.set_xlim(0, 200)
                ax.set_xticks([0, 100, 200])

            plt.tight_layout(rect=[0, 0, 1, 0.96])
            Path = os.path.join(self.OutputDir, f"{PrimaryItem}{FileSuffix}.png")
            plt.savefig(Path)
            plt.close(fig)

if __name__ == "__main__":
    Plotter = MetricsVisualiser()

    # Compare each method against each scenario
    Plotter.Plot(Plotter.Scenarios, Plotter.Methods, "Scenario", "Method", "_methods")

    # Compare each scenario against each method
    Plotter.Plot(Plotter.Methods, Plotter.Scenarios, "Method", "Scenario", "_scenarios")
