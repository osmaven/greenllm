
# Curso: Algoritmos Sostenibles para LLM (12 semanas)

Este repositorio incluye **sílabos, cronograma, rúbricas, laboratorios** y un **framework mínimo (Python)** para medir eficiencia energética y huella de carbono en *Large Language Models* (LLM), y para aplicar técnicas de **cuantización/destilación/serving eficiente**.

## Estructura

```
curso_algoritmos_sostenibles_llm/
├─ docs/                      # Sílabos, cronograma, políticas, rúbricas, bibliografía
├─ asignaciones/
│  ├─ reto1/                  # Definición y medición
│  ├─ reto2/                  # Framework de medición
│  └─ reto3/                  # Optimización (cuantización/destilación/serving)
├─ framework/                 # Paquete Python 'greenllm' + tests
│  ├─ pyproject.toml
│  ├─ src/greenllm/           # Código fuente del framework docente
│  └─ tests/
├─ scripts/                   # Scripts de benchmark/serving de ejemplo
├─ data/
│  ├─ prompts/                # Conjunto mínimo de prompts para pruebas
│  └─ eval/                   # Indicaciones para evaluación rápida de calidad
└─ notebooks/                 # Plantillas de cuadernos
```

## Inicio Rápido

1. **Crear entorno** (ej., conda o venv) y activar.
2. Instalar dependencias mínimas:  
   ```bash
   cd framework
   pip install -e .
   ```
   > Nota: para cuantización avanzada/serving acelerado se requieren paquetes opcionales (ver `docs/REQUISITOS.md`).

3. **Medir un modelo pequeño** (ejemplo usando *TinyLlama* para que funcione en GPU/CPU modesta):  
   ```bash
   greenllm measure      --model TinyLlama/TinyLlama-1.1B-Chat-v1.0      --prompts ../data/prompts/prompt_set_small.txt      --max-new-tokens 64      --meter nvml --carbon-intensity 300      --csv ../resultados_baseline.csv
   ```

4. **Explorar resultados**: el CSV incluye energía (J), latencia y métricas derivadas (**J/token**, **tokens/J**, **gCO₂e/1k tokens**).

5. **Rutas sugeridas**:
   - **Reto 1**: usa `greenllm measure` para definir y validar tus métricas y protocolo.
   - **Reto 2**: extiende el paquete `greenllm` (añade nuevas fuentes de carbono/medidores/exportadores).
   - **Reto 3**: compara antes/después con **cuantización/QLoRA/serving** y reporta **trade-offs**.

---
