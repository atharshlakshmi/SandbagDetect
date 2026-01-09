import csv
from pathlib import Path
from metrics import calculate_experiment_metrics

home = Path.home()

class Logger():
    """
    Logs each experiement with different models.
    """
    def __init__(self, model):
        self.model = model
        self.history = []

        self.full_path = home / "reports/experiment_logs" / model

        # headers for csv file
        self.headers = ["Question", "Evaluation Context", "Evaluation Response", "Casual Context", "Casual Response", "metric1", "metric2"]
        
        with open(self.full_path, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            
        print(f"Logger initialized. File created at: {self.full_path}")
    
    def log(self, responses, metrics):
        """
        Logs the metrics for each experiment and saves it into the Logger history.
        """
        pass

    def end(self, history):
        """
        Logs the metrics for the full experiment
        """
        calculate_experiment_metrics()
        pass
    


