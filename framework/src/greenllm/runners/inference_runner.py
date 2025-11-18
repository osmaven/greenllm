import random
from typing import List
from ..emeter.codecarbon_meter import CodeCarbonMeter
from ..metrics.evaluation import evaluar_modelos
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import numpy as np
from ..system_data.platform_data import get_system_info
import time
import datetime



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _read_prompts(path: str) -> List[List[str]]:
    """
    Lee un archivo de prompts y los agrupa por disciplina.
    
    Args:
        path (str): Ruta al archivo de prompts.

    Returns:
        List[List[str]]: Lista de dos elementos: 
            - prompts (List[str]): lista de prompts.
            - disciplinas (List[str]): lista de disciplinas correspondientes a cada prompt.
    """
    prompts = []
    disciplinas = []
    current_disciplina = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Detecta nueva disciplina por líneas entre corchetes
            if line.startswith("[") and line.endswith("]"):
                current_disciplina = line[1:-1].strip()
            elif current_disciplina:
                prompts.append(line)
                disciplinas.append(current_disciplina)
            else:
                raise ValueError(f"Línea fuera de sección: {line}")

    return [prompts, disciplinas]


def _load_model(model_name: str, precision: str):
    """
    Carga un modelo de lenguaje y su tokenizer con la precisión indicada.

    Args:
        model_name (str): Nombre o ruta del modelo.
        precision (str): "int8", "int4", "fp16", "bf16" o "auto".

    Returns:
        tuple: tokenizer y modelo cargados en el dispositivo (GPU o CPU).
    """
    kw = {}
    if precision == "int8":
        kw.update(dict(load_in_8bit=True))
    elif precision == "int4":
        try:
            kw.update(dict(load_in_4bit=True))
        except Exception:
            kw.update(dict(load_in_8bit=True))
    elif precision in ("fp16","bf16"):
        kw.update(dict(torch_dtype=torch.float16 if precision=="fp16" else torch.bfloat16))

    # Cargar tokenizer
    tok = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    # Cargar modelo y moverlo al dispositivo
    model = AutoModelForCausalLM.from_pretrained(model_name, **kw)
    model.to(device)
    return tok, model


def _generate_batch(tok, model, prompts, max_new_tokens=64):
    """
    Genera texto para un batch de prompts y calcula tokens generados.

    Args:
        tok: Tokenizer del modelo.
        model: Modelo cargado.
        prompts (list[str]): Lista de prompts.
        max_new_tokens (int): Máximo número de tokens a generar por prompt.

    Returns:
        tuple: (textos generados, número total de tokens generados)
    """
    # Tokenizar y mover a dispositivo
    batch = tok(prompts, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        out = model.generate(**batch, max_new_tokens=max_new_tokens)
    texts = tok.batch_decode(out, skip_special_tokens=True)

    # Calcular tokens generados por diferencia
    in_len = batch["input_ids"].shape[1]
    gen_tokens = sum(max(0, len(ids) - in_len) for ids in out)

    return texts, gen_tokens


def _get_meter(name: str, carbon_intensity):
    """
    Obtiene un medidor de consumo energético según el nombre.

    Args:
        name (str): Nombre del medidor, por ejemplo "codecarbon".
        carbon_intensity: Intensidad de carbono usada.

    Returns:
        instancia de medidor
    """
    if name == "codecarbon":
        return CodeCarbonMeter(carbon_intensity = carbon_intensity)




def measure_idle_power(meter_name:str="codecarbon", carbon_intensity = 'auto'):
    """
    Mide el consumo energético en estado idle durante 5 segundos.

    Args:
        meter_name (str): Nombre del medidor.
        carbon_intensity: Intensidad de carbono.

    Returns:
        float: Potencia en watts durante el estado idle.
    """
    meter = _get_meter(meter_name, carbon_intensity)
    meter.start()
    time.sleep(5)  # Tiempo de medición de idle
    m = meter.stop()
    w_idle = float(m.get("energy_w", 0.0)) * 3600 / float(m.get("duration_s", 0.0))
    return w_idle


def run_measurement(model_name: str, prompts_path: str, max_new_tokens: int=64, batch_size:int=1,
                    precision:str="auto", meter_name:str="codecarbon", carbon_intensity = 'auto', seed:int=42, n_iterations:int=1, verbose:bool = False) -> dict:
    """
    Ejecuta la medición de consumo energético y generación de texto del modelo sobre un conjunto de prompts.

    Args:
        model_name (str): Nombre o ruta del modelo.
        prompts_path (str): Archivo con prompts.
        max_new_tokens (int): Máximo número de tokens a generar.
        batch_size (int): Tamaño de los batches de prompts.
        precision (str): Precisión del modelo ("int8", "fp16", etc.).
        meter_name (str): Nombre del medidor de energía.
        carbon_intensity: Intensidad de carbono.
        seed (int): Semilla para reproducibilidad.
        n_iterations (int): Número de iteraciones a promediar.

    Returns:
        dict: Diccionario con resultados de generación, consumo energético, memoria, y evaluación.
    """

    if verbose:
        print(f"Usando dispositivo: {device}")
        if device.type == "cuda":
            print(f"GPU detectada: {torch.cuda.get_device_name(torch.cuda.current_device())}")


    random.seed(seed)

    # Leer prompts y disciplinas
    prompts_disciplinas = _read_prompts(prompts_path)
    prompts  = prompts_disciplinas[0]
    disciplinas = prompts_disciplinas[1]

    if not prompts:
        raise ValueError("No hay prompts en el archivo proporcionado.")

    return_dicts = []

    # Cargar modelo
    tok, model = _load_model(model_name, precision)

    # Medir uso de GPU si aplica
    if device.type == "cuda":
        gpu_memory_allocated = torch.cuda.memory_allocated() / (1024**2)  # MB
        gpu_memory_reserved = torch.cuda.memory_reserved() / (1024**2)    # MB
    else:
        gpu_memory_allocated = 0.0
        gpu_memory_reserved = 0.0

    # Warm-up para inicializar cachés de GPU y acelerar primera inferencia
    warmup_prompt = ["Prompt solo para warm-up."]
    _generate_batch(tok, model, warmup_prompt, max_new_tokens=max_new_tokens)

    for i in range(n_iterations):
        print(f'\033[32m[greenllm @ {datetime.datetime.now().strftime("%H:%M:%S")}]\033[0m Ejecutando iteración {i+1} de {n_iterations}')
        texts = []
        durations_s = []
        energies_w = []
        emissions_kg_tot = []
        tokens_generated = []
        w_idle = []

        w_idle.append(measure_idle_power(meter_name, carbon_intensity))

        # Procesar prompts en batches
        for i in range(0, len(prompts), batch_size):

            print(f'\033[32m[greenllm @ {datetime.datetime.now().strftime("%H:%M:%S")}]\033[0m Procesando prompts {i+1} a {min(i+batch_size, len(prompts))} de {len(prompts)}', end="\r")

            sub = prompts[i:i+batch_size]

            meter = _get_meter(meter_name, carbon_intensity)
            meter.start()

            batch_encoding = tok(sub, return_tensors="pt", padding=True).to(device)
            with torch.no_grad():
                out = model.generate(**batch_encoding, max_new_tokens=max_new_tokens)

            batch_texts = []
            batch_tokens_generated = []

            for i, ids in enumerate(out):
                prompt_len = batch_encoding["input_ids"][i].shape[0]  # tokens del prompt
                generated_ids = ids[prompt_len:]  # tokens generados por el modelo
                text = tok.decode(generated_ids, skip_special_tokens=True).strip()
                batch_texts.append(text)
                batch_tokens_generated.append(len(generated_ids))


            m = meter.stop()
            duration_s = float(m.get("duration_s", 0.0))
            energy_j = float(m.get("energy_w", 0.0))
            emissions_kg = m.get("emissions_kg", None)
            ci = m.get("carbon_intensity_used", None)

            # Guardar resultados
            texts.extend(batch_texts)
            durations_s.extend([duration_s] * len(sub))
            energies_w.extend([energy_j] * len(sub))
            emissions_kg_tot.extend([emissions_kg] * len(sub))
            tokens_generated.extend(batch_tokens_generated)
        
        print(f'\033[32m[greenllm @ {datetime.datetime.now().strftime("%H:%M:%S")}]\033[0m Ejecución {i+1} de {n_iterations} completada.      ')


        # Guardar resultados de esta iteración
        return_dict = {
            "model": model_name,
            "precision": precision,
            "meter": meter_name,
            "prompts_count": len(prompts),
            "batch_size": batch_size,
            "max_new_tokens": max_new_tokens,
            "energy_w": energies_w,
            "durations_s": durations_s,
            "tokens_generated": tokens_generated,
            "emissions_kg": emissions_kg_tot,
            "carbon_intensity_g_per_kwh": ci,
            "generated_texts": texts,
            "idle_power_w": np.mean(w_idle),
            "gpu_memory_allocated_mb": gpu_memory_allocated,
            "gpu_memory_reserved_mb": gpu_memory_reserved
        }

        return_dicts.append(return_dict)


    # Promediar resultados sobre n_iterations
    for key in ["energy_w", "durations_s", "tokens_generated", "emissions_kg"]:
        suma = [0.0] * len(return_dicts[0][key])
        for i in range(n_iterations):
            suma = [a + b for a, b in zip(suma, return_dicts[i][key])]
        return_dicts[0][key] = [s / n_iterations for s in suma]

    # Evaluar resultados generados
    print(f"\033[32m[greenllm]\033[0m Evaluando resultados generados con modelo oráculo")

    eval_scores = evaluar_modelos(prompts, disciplinas, texts, seed=seed, model="tngtech/deepseek-r1t2-chimera:free")
    agrupado = {}
    for valor, etiqueta in zip(eval_scores, disciplinas):
        agrupado.setdefault(etiqueta, []).append(valor)

    # Guardar evaluación y metadata
    return_dicts[0]["evaluation_scores"] = list(agrupado.values())
    return_dicts[0]["disciplines"] = list(agrupado.keys())
    return_dicts[0]["info"] = get_system_info()
    return_dicts[0]["n_iterations"] = n_iterations
    return_dicts[0]["seed"] = seed
    return_dicts[0]["idle_power_w"] = np.mean(w_idle)

    return return_dicts[0]
