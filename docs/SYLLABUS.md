
# Sílabos (12 semanas): Algoritmos sostenibles para LLM

- **Objetivo general:** que el alumnado defina **métricas de eficiencia/huella**, construya un **framework de medición** reproducible y **optimice** LLM mediante cuantización/destilación/serving eficiente con análisis de *trade-offs*.
- **Evaluación:** Reto 1 (25%), Reto 2 (35%), Reto 3 (40%). Laboratorios semanales obligatorios (entregables integrados en los Retos).
- **Prerequisitos:** Python, PyTorch, nociones de *transformers*, Linux y uso básico de GPU.

## Semana a semana

**Semana 1 — Introducción, ética y alcance**
- Impacto ambiental de IA; huella en entrenamiento vs. inferencia; *operational vs. embodied emissions*; PUE; límites del sistema.
- Laboratorio: entorno; modelos abiertos (p. ej., TinyLlama, OLMo, MPT); *hello world* de inferencia.
- Entrega: one-pager con límites del sistema y unidad funcional (p. ej., 1.000 tokens).

**Semana 2 — Medición de energía en CPU/GPU**
- Instrumentación directa (NVML, RAPL con pyJoules) y estimada (CodeCarbon).
- Laboratorio: medir potencia/energía durante *prefill/decoding* y loguear CSV/MLflow.
- Entrega: protocolo de medición (frecuencia, warm-up, repeticiones, estadísticos p50/p95).

**Semana 3 — Métricas sostenibles específicas para LLM**
- J/token, tokens/J, CO₂e/1k tokens, latencia, throughput, *tail latency*; calidad mínima (perplejidad o set de tareas ligero).
- Laboratorio: *baseline* con un modelo pequeño y cálculo de CO₂e en dos configuraciones.

**Semana 4 — Factores de emisión e incertidumbre**
- Intensidad de carbono horaria/regional; diferencias *location vs. marginal*; PUE.
- Laboratorio: repetir pruebas en dos franjas horarias; análisis de variabilidad.
- Cierre Reto 1: mini-paper (4–6 págs.).

**Semana 5 — Framework reproducible (I)**
- Diseño modular (runner/medidores/fuentes/exportadores); CLI; control de metadatos.
- Laboratorio: plantilla de paquete, primeras integraciones y pruebas de humo.
- Entrega: design doc + sprint backlog.

**Semana 6 — Framework reproducible (II)**
- Serving y carga: vLLM/TGI; batch y *long context*; trazabilidad de experimentos con MLflow.
- Laboratorio: servidor local y *bench* con distintas longitudes de contexto.
- Entrega: CLI funcional + dashboard MLflow.

**Semana 7 — Cuantización y QLoRA**
- PTQ vs. QAT; bitsandbytes (8/4-bit, NF4), GPTQ, AWQ; QLoRA.
- Laboratorio: cargar modelo 8/4-bit; medir memoria/latencia/energía y comparar calidad.

**Semana 8 — KV-cache y atención eficiente**
- Por qué domina coste; compresión y cuantización de KV-cache; kernels eficientes (FlashAttention).
- Laboratorio: prompts largos con/sin compresión; análisis de degradación.
- Cierre Reto 2: release v0.1 del framework.

**Semana 9 — Destilación y decodificación eficiente**
- Knowledge distillation hacia modelos pequeños; *speculative decoding* y variantes (p. ej., Medusa).
- Laboratorio: destilar subset instruct y comparar tokens/J vs. calidad.

**Semana 10 — Serving extremo y aceleradores**
- vLLM/TensorRT-LLM: *prefill/decoding* tuning, streaming, workers, afinidad CPU/GPU.
- Laboratorio: tuning y repetición de mediciones con el framework.

**Semana 11 — Carbono incorporado y decisiones de despliegue**
- Estimar M (fabricación/fin de vida) y prorrateo; planificación consciente del carbono.
- Laboratorio: escenarios con M bajo/alto y reporte SCI junto a métricas operacionales.

**Semana 12 — Presentaciones finales**
- Demo y paper (6–10 págs.): antes→después, gráficos, costes, guía de adopción.
- Cierre Reto 3.

## Resultados de aprendizaje

1) Definir métricas y SCI aplicadas a LLM; 2) Medir energía/CO₂e con trazabilidad; 3) Diseñar un framework reproducible; 4) Optimizar con técnicas modernas justificando *trade-offs*.
