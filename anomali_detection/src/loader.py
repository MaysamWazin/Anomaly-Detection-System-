import csv
from pathlib import Path
from typing import List

from .models import NetworkRecord


class CsvLoader:
    """
    dataSet.csv dosyasını okur ve NetworkRecord listesine çevirir.

    Beklenen sütun isimleri (senin veri setine göre):
    - packet_size
    - inter_arrival_time
    - src_port
    - dst_port
    - packet_count_5s
    - mean_packet_size
    - spectral_entropy
    - frequency_band_energy
    - label
    - (diğer sütunlar varsa okunmaz, sorun değil)
    """

    def load(self, path: Path) -> List[NetworkRecord]:
        records: List[NetworkRecord] = []

        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            print("[DEBUG] Sütun isimleri:", reader.fieldnames)

            error_count = 0

            for idx, row in enumerate(reader):
                try:
                    packet_size = float(row["packet_size"])
                    inter_arrival_time = float(row["inter_arrival_time"])
                    src_port = int(float(row["src_port"]))
                    dst_port = int(float(row["dst_port"]))
                    packet_count_5s = float(row["packet_count_5s"])
                    mean_packet_size = float(row["mean_packet_size"])
                    spectral_entropy = float(row["spectral_entropy"])
                    frequency_band_energy = float(row["frequency_band_energy"])
                    label = int(float(row["label"]))  # 0.0 / 1.0 -> 0 / 1

                    record = NetworkRecord(
                        index=idx,
                        packet_size=packet_size,
                        inter_arrival_time=inter_arrival_time,
                        src_port=src_port,
                        dst_port=dst_port,
                        packet_count_5s=packet_count_5s,
                        mean_packet_size=mean_packet_size,
                        spectral_entropy=spectral_entropy,
                        frequency_band_energy=frequency_band_energy,
                        label=label,
                    )
                    records.append(record)

                except Exception as e:
                    error_count += 1
                    if error_count <= 5:
                        print(f"[DEBUG] Satır {idx + 2} parse hatası: {e}")
                        print("[DEBUG] Satır içeriği:", row)
                    continue

        print(
            f"[DEBUG] Başarıyla yüklenen kayıt sayısı: {len(records)}, "
            f"hata sayısı: {error_count}"
        )
        return records
