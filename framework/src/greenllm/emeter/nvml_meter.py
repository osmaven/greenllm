
import time, threading

class NvmlMeter:
    """
    Muestreador de potencia GPU vía pynvml (NVML). Acumula energía (J).
    Si NVML no está disponible, retorna 0.
    """
    def __init__(self, interval=0.1, device_index=0):
        self.interval = interval
        self.device_index = device_index
        self._running = False
        self._thread = None
        self._energy_j = 0.0
        self._start_ts = None
        try:
            import pynvml
            self._available = True
            self._nvml = pynvml
            self._nvml.nvmlInit()
            self._handle = self._nvml.nvmlDeviceGetHandleByIndex(self.device_index)
        except Exception:
            self._available = False
            self._nvml = None
            self._handle = None

    def _loop(self):
        # Integra potencia (W) en el tiempo => energía (J)
        last = time.time()
        while self._running:
            now = time.time()
            dt = now - last
            last = now
            try:
                if self._available:
                    p_mw = self._nvml.nvmlDeviceGetPowerUsage(self._handle)  # mili-watts
                    power_w = p_mw / 1000.0
                else:
                    power_w = 0.0
            except Exception:
                power_w = 0.0
            self._energy_j += power_w * dt
            time.sleep(self.interval)

    def start(self):
        self._energy_j = 0.0
        self._running = True
        self._start_ts = time.time()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
        duration = (time.time() - self._start_ts) if self._start_ts else 0.0
        return {"energy_j": self._energy_j, "duration_s": duration}
