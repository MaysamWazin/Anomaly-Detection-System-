from typing import List
import csv
from pathlib import Path

from .models import AnomalyResult


class Reporter:
    def print_summary(self, anomalies: List[AnomalyResult]) -> None:
        total_records = len(anomalies)
        algo_anomaly_count = sum(1 for a in anomalies if a.is_anomaly)
        label_anomaly_count = sum(1 for a in anomalies if a.record.label == 1)


        tp = sum(1 for a in anomalies if a.is_anomaly and a.record.label == 1)
        fp = sum(1 for a in anomalies if a.is_anomaly and a.record.label == 0)
        fn = sum(1 for a in anomalies if (not a.is_anomaly) and a.record.label == 1)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        print()
        print("========= ANOMALY DETECTION RAPORU =========")
        print(f"Toplam kayıt sayısı           : {total_records}")
        print(f"Etiketli anomali sayısı (label=1): {label_anomaly_count}")
        print(f"Algoritmanın bulduğu anomali sayısı: {algo_anomaly_count}")
        print("--------------------------------------------")
        print(f"True Positive (TP)  : {tp}")
        print(f"False Positive (FP) : {fp}")
        print(f"False Negative (FN) : {fn}")
        print("--------------------------------------------")
        print(f"Precision (TP / (TP+FP)) : {precision:.3f}")
        print(f"Recall    (TP / (TP+FN)) : {recall:.3f}")
        print(f"F1-Score                 : {f1:.3f}")
        print("--------------------------------------------")

        top_anomalies = sorted(
            anomalies, key=lambda a: abs(a.z_score), reverse=True
        )[:10]

        if not any(a.is_anomaly for a in anomalies):
            print("[+] Eşik değerine göre anomali tespit edilmedi.")
            return

        print("[+] Örnek anomaliler (ilk 10, |z| büyükten küçüğe):")
        for a in top_anomalies:
            r = a.record
            status = (
                "GERÇEK ANOMALİ (label=1)"
                if r.label == 1
                else "label=0 (normal olarak etiketli)"
            )
            print(
                f"Index: {r.index}, "
                f"score={r.score:.3f}, z={a.z_score:.2f}, "
                f"algoritma_anomali={a.is_anomaly}, {status}"
            )

    def export_to_csv(self, anomalies: List[AnomalyResult], output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "index",
                    "packet_size",
                    "inter_arrival_time",
                    "src_port",
                    "dst_port",
                    "packet_count_5s",
                    "mean_packet_size",
                    "spectral_entropy",
                    "frequency_band_energy",
                    "label",
                    "score",
                    "z_score",
                    "is_anomaly",
                    "reason",
                ]
            )

            for a in anomalies:
                r = a.record
                writer.writerow(
                    [
                        r.index,
                        f"{r.packet_size:.6f}",
                        f"{r.inter_arrival_time:.6f}",
                        r.src_port,
                        r.dst_port,
                        f"{r.packet_count_5s:.6f}",
                        f"{r.mean_packet_size:.6f}",
                        f"{r.spectral_entropy:.6f}",
                        f"{r.frequency_band_energy:.6f}",
                        r.label,
                        f"{r.score:.6f}",
                        f"{a.z_score:.6f}",
                        1 if a.is_anomaly else 0,
                        a.reason.replace(",", ";"),
                    ]
                )
