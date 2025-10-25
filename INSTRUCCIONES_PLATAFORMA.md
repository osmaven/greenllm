# Guía de Inicio Rápido por Plataforma

Esta guía contiene las órdenes exactas para configurar y ejecutar el proyecto en diferentes sistemas operativos.

---

## Paso 1: Explorar la documentación web

Para visualizar la documentación del curso de forma cómoda, puedes abrir el sitio web local en tu navegador.

### macOS / Linux
```bash
open website/index.html
```

### Windows
```bash
start website/index.html
```

---

## Paso 2: Configurar el entorno de Python

Es fundamental crear un entorno virtual para instalar las dependencias del proyecto de forma aislada.

### macOS / Linux
```bash
# 1. Crea un entorno virtual llamado 'venv'
python3 -m venv venv

# 2. Activa el entorno virtual
source venv/bin/activate
```

### Windows
```bash
# 1. Crea un entorno virtual llamado 'venv'
python -m venv venv

# 2. Activa el entorno virtual
.\\venv\\Scripts\\activate
```

---

## Paso 3: Instalar el framework `greenllm`

Con el entorno activado, instala el paquete `greenllm` en modo editable. Esto permite que los cambios en el código se reflejen al instante.

```bash
# 1. Navega al directorio del framework
cd framework

# 2. Instala el paquete y sus dependencias
pip install -e .

# 3. Regresa al directorio raíz del proyecto
cd ..
```
*(Este paso es idéntico para todos los sistemas operativos).*

---

## Paso 4: Ejecutar la primera medición

Finalmente, ejecuta tu primera medición de un modelo LLM. Este comando usa `TinyLlama` (un modelo pequeño), mide con `nvml` (para GPUs NVIDIA) y guarda los resultados en un archivo CSV.

```bash
# Ejecuta la medición de energía y rendimiento
greenllm measure \
    --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
    --prompts data/prompts/prompt_set_small.txt \
    --max-new-tokens 64 \
    --meter nvml \
    --carbon-intensity 300 \
    --csv resultados_baseline.csv
```
*(Este comando es idéntico para todos los sistemas operativos. Si no tienes una GPU NVIDIA, puedes cambiar `--meter nvml` por `--meter codecarbon` o `--meter pyjoules` según lo que hayas configurado).*

---

Tras ejecutar este último comando, encontrarás un archivo `resultados_baseline.csv` en el directorio raíz con todas las métricas de la medición.

---

## Anexo: Otros Modelos Pequeños para Testear

Para tus experimentos, es recomendable usar modelos que no requieran hardware muy potente. Aquí tienes una lista de modelos "pequeños" (generalmente por debajo de 3 mil millones de parámetros) que son ideales para empezar. Todos se descargan automáticamente desde el Hugging Face Hub.

Simplemente reemplaza el nombre del modelo en el comando `greenllm measure`.

*   **`TinyLlama/TinyLlama-1.1B-Chat-v1.0`**: El modelo base de los ejemplos. Muy ligero.
*   **`microsoft/phi-2`**: Un modelo de ~2.7B de parámetros muy popular por su alta calidad para su tamaño.
*   **`google/gemma-2b-it`**: La versión de 2.5B de parámetros de la familia Gemma de Google, optimizada para chat.
*   **`princeton-nlp/Sheared-LLaMA-1.3B`**: Una versión más pequeña y eficiente de LLaMA.
*   **`stabilityai/stablelm-2-1_6b-chat`**: Un modelo reciente de 1.6B de parámetros de Stability AI.

**Ejemplo de uso con `phi-2`:**
```bash
greenllm measure \
    --model microsoft/phi-2 \
    --prompts data/prompts/prompt_set_small.txt \
    ...
```
