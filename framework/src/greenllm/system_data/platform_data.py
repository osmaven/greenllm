import platform
import psutil
import torch

def get_system_info() -> dict:
    info = {}
    # Recolectar información básica del sistema
    info["os"] = platform.system()
    info["os_version"] = platform.version()
    info["python_version"] = platform.python_version()
    info["machine"] = platform.machine()
    info["processor"] = platform.processor()
    info["cpu_count"] = psutil.cpu_count(logical=True)
    info["cpu_physical_count"] = psutil.cpu_count(logical=False)
    info["total_ram_gb"] = round(psutil.virtual_memory().total / (1024**3), 2)

    # Intentar obtener información de GPU (si hay CUDA o CodeCarbon la detecta)
    info["gpu_available"] = torch.cuda.is_available()
    if torch.cuda.is_available():
        gpus = []
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            gpus.append({
                "index": i,
                "name": props.name,
                "total_memory_gb": round(props.total_memory / (1024**3), 2),
                "compute_capability": f"{props.major}.{props.minor}",
            })
        info["gpus"] = gpus

    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    info["processor_model"] = line.strip().split(":")[1].strip()

    except:
        
        info["processor_model"] = "Desconocido"


    return info


print(get_system_info())