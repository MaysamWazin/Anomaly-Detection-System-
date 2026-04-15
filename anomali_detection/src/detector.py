from typing import List
import math

from .models import NetworkRecord, AnomalyResult


class ZScoreAnomalyDetector:
    """
    Z-Score tabanlı basit anomaly detection.

    Her kayıt için:
        score = packet_size + frequency_band_energy

    Tüm kayıtlar üzerinden:
        mean = skorların ortalaması
        std  = skorların standart sapması

        z = (score - mean) / std

    |z| >= threshold ise --> anomali
    """

    def __init__(self, threshold: float = 1.5):
        if threshold <= 0:
            raise ValueError("Z-Score threshold pozitif olmalıdır.")
        self.threshold = threshold

    def detect(self, records: List[NetworkRecord]) -> List[AnomalyResult]:
        if not records:
            raise ValueError("Kayıt listesi boş olamaz.")

        scores = [r.score for r in records]
        mean = sum(scores) / len(scores)
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)
        std_dev = math.sqrt(variance)

        if std_dev <= 0:
            std_dev = 1.0  # tüm skorlar aynı ise

        results: List[AnomalyResult] = []

        for rec in records:
            z = (rec.score - mean) / std_dev
            abs_z = abs(z)
            is_anomaly = abs_z >= self.threshold

            if is_anomaly:
                reason = f"|z|={abs_z:.2f} >= {self.threshold}"
            else:
                reason = "Normal"

            results.append(
                AnomalyResult(
                    record=rec,
                    z_score=z,
                    is_anomaly=is_anomaly,
                    reason=reason,
                )
            )

        return results
