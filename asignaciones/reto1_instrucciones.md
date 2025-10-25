
# Reto 1 — Definir y medir eficiencia/huella en LLM

**Objetivo:** Proponer un conjunto de métricas y un protocolo experimental para evaluar eficiencia energética y huella de carbono en LLM, y validarlo con un *baseline* reproducible.

## Entregables
1. Documento (4–6 págs.) con:
   - Unidad funcional (p. ej., 1.000 tokens generados).
   - Métricas: J/token, tokens/J, gCO₂e/1k tokens, latencia p50/p95, throughput, calidad mínima.
   - Protocolo: frecuencia de muestreo, warm-up, nº de repeticiones, control de ruido.
   - Fuentes de intensidad de carbono y PUE (supuestos y límites).
2. Scripts/configs para reproducir el *baseline* con `greenllm measure`.
3. CSV con resultados y breve análisis estadístico.

## Criterios de aceptación
- Repetibilidad N≥5 y reporte de IC/percentiles.
- Trazabilidad: commits, seeds, versiones, hardware.
- Comparabilidad: misma carga en configuraciones A/B.

## Entrega
- Repositorio con `/experiments/baseline/` y README ejecutable.
