
# greenllm (docente)

Pequeño framework para medir energía/CO₂e y evaluar optimizaciones en LLM.

## Instalación de desarrollo
```bash
pip install -e .
```

## Uso rápido
```bash
greenllm measure --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --prompts ../data/prompts/prompt_set_small.txt --max-new-tokens 64 --meter nvml --carbon-intensity 300 --csv ../resultados.csv
```
