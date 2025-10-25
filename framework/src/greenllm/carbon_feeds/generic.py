
import os

def get_carbon_intensity(default=None):
    """
    Devuelve intensidad de carbono (gCO2e/kWh).
    - Si la variable de entorno CARBON_INTENSITY_G_PER_KWH está fijada, se usa.
    - Si no, retorna el 'default' (puede venir desde CLI).
    """
    v = os.getenv("CARBON_INTENSITY_G_PER_KWH", None)
    if v is not None:
        try:
            return float(v)
        except Exception:
            pass
    return default
