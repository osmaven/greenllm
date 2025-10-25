
import time
class CodeCarbonMeter:
    """
    Envoltorio mínimo alrededor de CodeCarbon (EmissionsTracker).
    Si no está instalado, devuelve energía 0 y emisiones 0.
    """
    def __init__(self, country_iso_code=None, measure_power_secs=1.0):
        self._start = None
        try:
            from codecarbon import EmissionsTracker
            self._available = True
            self._tracker = EmissionsTracker(measure_power_secs=measure_power_secs,
                                             country_iso_code=country_iso_code)
        except Exception:
            self._available = False
            self._tracker = None

    def start(self):
        self._start = time.time()
        if self._available:
            self._tracker.start()

    def stop(self):
        emissions = 0.0
        energy_kwh = 0.0
        if self._available:
            emissions = self._tracker.stop() or 0.0
            try:
                energy_kwh = float(self._tracker.final_emissions_data.energy_consumed)
            except Exception:
                energy_kwh = 0.0
        duration = (time.time() - self._start) if self._start else 0.0
        return {"energy_j": energy_kwh * 3600000.0, "duration_s": duration, "emissions_kg": emissions}
