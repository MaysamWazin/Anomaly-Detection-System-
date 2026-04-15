from dataclasses import dataclass


@dataclass
class NetworkRecord:
    """
    Veri setindeki her bir satırı temsil eder.
    Kullandığımız sütunlar:

    - packet_size
    - inter_arrival_time
    - src_port
    - dst_port
    - packet_count_5s
    - mean_packet_size
    - spectral_entropy
    - frequency_band_energy
    - label (0 = normal, 1 = anomali)
    """

    index: int 
    packet_size: float
    inter_arrival_time: float
    src_port: int
    dst_port: int
    packet_count_5s: float
    mean_packet_size: float
    spectral_entropy: float
    frequency_band_energy: float
    label: int  

    @property
    def score(self) -> float:
        """
        Anomali tespiti için kullandığımız sayısal skor.
        Burada basitçe:
            score = packet_size + frequency_band_energy
        """
        return self.packet_size + self.frequency_band_energy


@dataclass
class AnomalyResult:
    """
    Anomali tespit sonucu:
    - record: hangi kayıt
    - z_score: hesaplanan z-score
    - is_anomaly: threshold'u geçiyor mu
    - reason: açıklama
    """

    record: NetworkRecord
    z_score: float
    is_anomaly: bool
    reason: str
