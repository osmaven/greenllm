
import csv, os, datetime

class CSVExporter:
    def __init__(self, path):
        self.path = path

    def export(self, payload: dict):
        # Aplana primer nivel de dicts simples
        flat = {}
        for k, v in payload.items():
            if isinstance(v, (int, float, str)) or v is None:
                flat[k] = v
        is_new = not os.path.exists(self.path)
        with open(self.path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp"] + list(flat.keys()))
            if is_new:
                writer.writeheader()
            writer.writerow({"timestamp": datetime.datetime.utcnow().isoformat(), **flat})
