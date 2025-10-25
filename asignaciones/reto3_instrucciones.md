
# Reto 3 — Optimización y reducción de huella

**Objetivo:** Aplicar ≥2 técnicas (p. ej., INT8/INT4, GPTQ/AWQ, QLoRA, compresión de KV-cache, atención/decodificación eficiente, tuning de serving) y mostrar mejoras significativas en **tokens/J** y **gCO₂e/1k tokens** a **paridad de calidad**.

## Requisitos
- Reporte *antes→después* con calidad, latencia p50/p95, throughput, memoria, energía (J), CO₂e, SCI estimado.
- Discusión de *trade-offs* (precisión vs. eficiencia, latencia vs. throughput).
- Scripts y configs reproducibles.

## Entregables
- Informe (6–10 págs.) con gráficos y tablas.
- Carpeta `experiments/opt/` con *scripts* y resultados.
