from pathlib import Path

from flask import Flask, render_template, request

from src.loader import CsvLoader
from src.detector import ZScoreAnomalyDetector


app = Flask(__name__)


def run_detection(threshold: float = 1.5):

    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    csv_path = data_dir / "dataSet.csv"

    loader = CsvLoader()
    records = loader.load(csv_path)

    total_records = len(records)
    label_anomaly_count = sum(1 for r in records if r.label == 1)

    detector = ZScoreAnomalyDetector(threshold=threshold)
    results = detector.detect(records)

    algo_anomaly_count = sum(1 for a in results if a.is_anomaly)

   
    tp = sum(1 for a in results if a.is_anomaly and a.record.label == 1)
    fp = sum(1 for a in results if a.is_anomaly and a.record.label == 0)
    fn = sum(1 for a in results if (not a.is_anomaly) and a.record.label == 1)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    top_anomalies = sorted(
        results, key=lambda a: abs(a.z_score), reverse=True
    )[:20]

    context = {
        "total_records": total_records,
        "label_anomaly_count": label_anomaly_count,
        "algo_anomaly_count": algo_anomaly_count,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "threshold": threshold,
        "anomalies": top_anomalies,
    }

    return context


@app.route("/", methods=["GET", "POST"])
def index():
    
    threshold = 1.5

    if request.method == "POST":
        try:
            threshold = float(request.form.get("threshold", "1.5").replace(",", "."))
        except ValueError:
            threshold = 1.5

    context = run_detection(threshold)
    return render_template("index.html", **context)


if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=True)
