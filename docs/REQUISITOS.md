
# Requisitos y recomendaciones de entorno

- Python 3.10+ (recomendado 3.11)
- GPU NVIDIA con drivers recientes (para NVML y aceleración). CPU/Apple Silicon funcionan con modelos pequeños.
- Paquetes principales: `torch`, `transformers`, `accelerate`, `bitsandbytes`, `mlflow`, `codecarbon`, `pynvml`.
- Opcionales: `pyJoules` (RAPL CPU/DRAM), `auto-gptq`, `awq`, `vllm`, `tensorrt-llm`.
- Usa modelos ligeros para probar (p. ej., `TinyLlama/TinyLlama-1.1B-Chat-v1.0`).

> Consejos: fija *seeds*, realiza warm-up, repite N≥5, reporta intervalos de confianza.
