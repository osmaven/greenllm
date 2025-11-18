import json
import os
import datetime

class JSONExporter:
    def __init__(self, path: str):
        self.path = path

    def export(self, payload: dict):
        """
        Guarda el payload en un archivo JSON con formato legible.
        Si la ruta no existe, la crea automáticamente.
        """
        # Crear carpeta si hay un directorio en la ruta
        dir_name = os.path.dirname(self.path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        # Agregar metadatos de exportación
        export_data = {
            "exported_at": datetime.datetime.now().isoformat(),
            "payload": payload
        }

        # Guardar como JSON con formato bonito (indentado)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Archivo JSON guardado: {os.path.abspath(self.path)}")
