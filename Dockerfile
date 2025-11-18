FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-runtime

WORKDIR /app

# --- Instala herramientas útiles ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    python3-dev \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# --- Actualiza pip y añade 'uv' (tu gestor) ---
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir uv

# --- Instala tu framework (editable mode) ---
COPY framework ./framework
RUN cd framework && uv pip install --system -e .

# --- Instala PyNVML y cualquier otra dependencia global ---
RUN pip install --no-cache-dir pynvml numpy

# --- Copia el resto del proyecto ---
COPY . .

# --- Mantiene el contenedor en ejecución (modo desarrollo) ---
CMD ["tail", "-f", "/dev/null"]
