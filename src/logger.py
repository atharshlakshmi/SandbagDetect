import csv
from pathlib import Path
import sys
import re

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.metrics import calculate_experiment_metrics

home = Path(__file__).parent.parent

class Logger():
    """
    Logs each experiement with different models.
    """
    def __init__(self, model):
        self.model = model
        self.history = []

        safe_model_name = re.sub(r'[\\/*?:"<>|]', "_", model)

        # Create reports directory if it doesn't exist
        reports_dir = home / "reports" / "experiment_logs"
        reports_dir.mkdir(parents=True, exist_ok=True)

        self.file_path = reports_dir / f"{safe_model_name}.csv"

        # headers for csv file
        self.headers = ["question",
            "evaluation_context",
            "evaluation_context_response",
            "casual_context",
            "casual_context_response",
            "eval_correct",
            "casual_correct",
            "correctness_diff",
            "length_ratio",
            "semantic_similarity",
            "sandbagging_flag"]
        
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            
        print(f"Logger initialized. File created at: {self.file_path}")
    
    def log(self, responses, metrics, pair):
        """
        Logs the metrics for each experiment and saves it into the Logger history.
        """

        # Build the row to write
        row = {
            "question": pair.get("question", ""),
            "evaluation_context": pair.get("evaluation_context", ""),
            "evaluation_context_response": responses.get("evaluation_context_response", ""),
            "casual_context": pair.get("casual_context", ""),
            "casual_context_response": responses.get("casual_context_response", ""),
            "eval_correct": metrics.get("eval_correct", ""),
            "casual_correct": metrics.get("casual_correct", ""),
            "correctness_diff": metrics.get("correctness_diff", ""),
            "length_ratio": metrics.get("length_ratio", ""),
            "semantic_similarity": metrics.get("semantic_similarity", ""),
            "sandbagging_flag": metrics.get("sandbagging_flag", ""),
        }


        # Append the row to the CSV and save in-memory history
        with open(self.file_path, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(row)

        self.history.append(row)

        print(f"Logged Prompt Pair {len(self.history)}")

    def end(self, history):
        """
        Logs the metrics for the full experiment
        Stored in a seperate CSV so as to compare each model
        """
        try:
            final_metrics = calculate_experiment_metrics(history) or {}
        except Exception:
            final_metrics = {}

        path = home / 'reports/experiment_logs/model_comparison.csv'

        # If final_metrics is available, use its keys as the CSV headers
        if final_metrics:
            comparison_headers = ["Model"] + list(final_metrics.keys())
        else:
            # Fallback headers
            comparison_headers = [
                "model",
                "eval_correctness",
                "casual_correctness",
                "accuracy_drop",
                "sandbagging_rate",
                "sandbagging_confidence",
                "semantic_similarity_mean",
                "semantic_similarity_std",
                "length_ratio_mean",
                "t_stat",
                "p_value",
                "significant_divergence",
            ]

        # Build the row mapping header 
        row = {"Model": self.model}
        for key in comparison_headers[1:]:
            val = final_metrics.get(key, "") if final_metrics else ""
            if val is None:
                row[key] = ""
            else:
                try:
                    # numpy scalar -> python scalar
                    row[key] = val.item()
                except Exception:
                    row[key] = val

        write_header = not path.exists()
        with open(path, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=comparison_headers)
            if write_header:
                writer.writeheader()
            writer.writerow(row)



