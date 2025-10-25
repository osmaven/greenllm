
import time

class PyJoulesMeter:
    """
    Medidor simple usando pyJoules (si está disponible). Si no, devuelve energía 0.
    """
    def __init__(self, domains=None):
        self.domains = domains or []
        self._start = None
        self._energy_j = 0.0
        try:
            from pyJoules.energy_meter import EnergyMeter
            from pyJoules.device.rapl_device import RaplPackageDomain, RaplDramDomain
            self._available = True
            self._meter = EnergyMeter([RaplPackageDomain(0), RaplDramDomain(0)])
        except Exception:
            self._available = False
            self._meter = None

    def start(self):
        self._start = time.time()
        if self._available:
            self._meter.start()

    def stop(self):
        if self._available:
            self._meter.stop()
            samples = self._meter.get_trace()
            # Sumatorio simple de energía (J)
            total = 0.0
            for e in samples:
                for m in e.energy:
                    total += m.energy
            self._energy_j = float(total)
        else:
            self._energy_j = 0.0
        return {"energy_j": self._energy_j, "duration_s": (time.time() - self._start)}
