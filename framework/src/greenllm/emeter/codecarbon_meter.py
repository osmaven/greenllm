
import time

class CodeCarbonMeter():
    """
    
    Medidor de emisiones de carbono utilizando CodeCarbon.
    """

    def __init__(self, measure_power_secs=0.1, carbon_intensity='auto', verbose=False):
        self._start = None
        self._carbon_intensity = carbon_intensity
        try:

            import logging
            from codecarbon import EmissionsTracker
            logging.getLogger("codecarbon").setLevel(logging.ERROR)

            self._available = True
            self._tracker = EmissionsTracker(measure_power_secs=measure_power_secs, log_level = "critical" if not verbose else "info")

        except Exception as e:
            print("CodeCarbon no está disponible. No se medirán las emisiones. Exception:", e)
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

        if self._carbon_intensity == 'auto':

            return {"energy_w": energy_kwh * 1000.0, "duration_s": duration, "emissions_kg": emissions}
        
        else: 
            
            return {"energy_w": energy_kwh * 1000.0, "duration_s": duration, "emissions_kg": energy_kwh * float(self._carbon_intensity) / 1000.0}