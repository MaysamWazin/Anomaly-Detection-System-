from pathlib import Path

from src.loader import CsvLoader
from src.detector import ZScoreAnomalyDetector
from src.report import Reporter


def main():
    print("=== Anomaly Detection System (Z-Score Based) ===")

    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    csv_path = data_dir / "dataSet.csv"

    if not csv_path.exists():
        print(f"[HATA] Veri dosyası bulunamadı: {csv_path}")
        print("Lütfen data klasörü içinde dataSet.csv dosyasının olduğundan emin ol.")
        input("Çıkmak için Enter'a bas...")
        return


    loader = CsvLoader()
    records = loader.load(csv_path)

    print(f"[+] Toplam kayıt sayısı        : {len(records)}")

    if not records:
        print("[!] Hiç kayıt yüklenemedi, program sonlandırılıyor.")
        input("Çıkmak için Enter'a bas...")
        return

    num_label_anom = sum(1 for r in records if r.label == 1)
    print(f"[+] Etiketli anomali sayısı    : {num_label_anom}")
    print(f"[+] Etiketli normal kayıt sayısı: {len(records) - num_label_anom}")

    z_threshold = 1.5
    detector = ZScoreAnomalyDetector(threshold=z_threshold)
    print(f"[+] Z-Score eşik değeri        : {z_threshold}")

 
    anomalies = detector.detect(records)


    reporter = Reporter()
    reporter.print_summary(anomalies)

    output_path = data_dir / "anomalies_output.csv"
    reporter.export_to_csv(anomalies, output_path)
    print(f"[+] Anomali sonuçları '{output_path}' dosyasına kaydedildi.")

    print("\n[+] Program tamamlandı. Çıkmak için Enter'a bas...")
    input()


if __name__ == "__main__":
    main()
