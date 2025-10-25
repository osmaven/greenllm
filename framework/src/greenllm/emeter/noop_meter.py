
import time
class NoOpMeter:
    """ Medidor nulo: energía 0 (útil para depurar o si no hay permisos). """
    def start(self): self._t = time.time()
    def stop(self): 
        import time
        return {"energy_j": 0.0, "duration_s": (time.time() - getattr(self, "_t", time.time()))}
