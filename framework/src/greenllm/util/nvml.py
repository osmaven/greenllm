
def get_gpu_info():
    """
    Devuelve info básica de GPU vía NVML, si está disponible.
    """
    try:
        import pynvml
        pynvml.nvmlInit()
        count = pynvml.nvmlDeviceGetCount()
        infos = []
        for i in range(count):
            h = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(h).decode("utf-8")
            mem = pynvml.nvmlDeviceGetMemoryInfo(h)
            infos.append({"index": i, "name": name, "memory_total": mem.total})
        return infos
    except Exception:
        return []
