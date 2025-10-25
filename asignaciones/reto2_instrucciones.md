
# Reto 2 — Framework de medición reproducible

**Objetivo:** Desarrollar una librería/CLI que ejecute inferencia de LLM, mida energía/potencia, integre factores de carbono y exporte resultados (CSV/MLflow).

## Requisitos mínimos
- Módulos: runner, medidores (NVML/CodeCarbon/pyJoules), fuentes de carbono (constante/env/API), exportadores (CSV/MLflow).
- CLI: `greenllm measure ...` con parámetros clave (modelo, prompts, tokens, batch, meter, intensidad, salida).
- Registro de metadatos (HW, versión modelo, *commit*, *seeds*).
- Tests de humo y documentación.

## Entregables
- Paquete `greenllm` instalable (`pip install -e .`).
- Ejemplos reproducibles en `/experiments/`.
- Dashboard MLflow opcional.

