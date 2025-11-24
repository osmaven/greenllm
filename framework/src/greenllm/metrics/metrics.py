import numpy as np


#Separa una lista plana en sublistas según la estructura dada (usado para tener según disciplinas)
def split_by_structure(flat_list, structure):
    result, idx = [], 0
    for sub in structure:
        n = len(sub)
        result.append(flat_list[idx: idx + n])
        idx += n
    return result


def compute_metrics(results: dict) -> dict:
    """
    A partir de resultados brutos (energía J, tokens, latencias), devuelve métricas derivadas agrupadas por disciplina.
    Espera claves: energy_w, tokens_generated, durations_s, evaluation_scores (lista de listas).
    """
    energy_w = results.get("energy_w", [])
    tokens = results.get("tokens_generated", [])
    durations = results.get("durations_s", [])
    eval_scores = results.get("evaluation_scores", [])



    # --- Energía y tokens ---
    w_per_token = [(e / t) if (t and t > 0) else None for e, t in zip(energy_w, tokens)]
    tokens_per_w = [(t / e) if (e and e > 0) else None for t, e in zip(tokens, energy_w)]
    w_per_1k_tokens = [(w / (t / 1000)) if (t and t > 0) else None for w, t in zip(energy_w, tokens)]

    j_per_token = [w * 3600 for w in w_per_token] 
    tokens_per_w = [w / 3600 for w in tokens_per_w] 
    j_per_1k_tokens = [w * 3600 for w in w_per_1k_tokens]


    # --- CO2e estimado (si hay intensidad y/o emissions_kg de CodeCarbon) ---
    kg_co2 = results["emissions_kg"] 
    g_co2 = [(c * 1000) if c is not None else None for c in kg_co2]

    # --- Normalización por 1k tokens ---
    co2e_per_1k = [(c / (t / 1000)) if (c is not None and t and t > 0) else None for c, t in zip(g_co2, tokens)]

    # --- Nueva métrica: tokens/segundo ---
    tokens_per_s = [(t / d) if (d and d > 0) else None for t, d in zip(tokens, durations)]




    grouped_metrics = {
        
        "run_info": {
            "model": results.get("model", None),
            "precision": results.get("precision", None),
            "meter": results.get("meter", None),
            "prompts_count": results.get("prompts_count", None),
            "batch_size": results.get("batch_size", None),
            "max_new_tokens": results.get("max_new_tokens", None),
            "idle_power_w": results.get("idle_power_w", None),
            "gpu_memory_allocated_mb": results.get("gpu_memory_allocated_mb", None),
            "gpu_memory_reserved_mb": results.get("gpu_memory_reserved_mb", None),
            "system_info": results.get("info", None),
            "disciplines": results.get("disciplines", []),
            "generated_texts": results.get("generated_texts", None),

        },

        "metrics": {
            "w_per_token": split_by_structure(w_per_token, eval_scores),
            "tokens_per_wat": split_by_structure(tokens_per_w, eval_scores),
            "j_per_token": split_by_structure(j_per_token, eval_scores),
            "tokens_per_j": split_by_structure(tokens_per_w, eval_scores),
            "w_per_1k_tokens": split_by_structure(w_per_1k_tokens, eval_scores),
            "j_per_1k_tokens": split_by_structure(j_per_1k_tokens, eval_scores),
            "co2e_g_total": split_by_structure(g_co2, eval_scores),
            "co2e_g_per_1k_tokens": split_by_structure(co2e_per_1k, eval_scores),
            "evaluation_scores": eval_scores,
            "tokens_per_second": split_by_structure(tokens_per_s, eval_scores), 
        }
    }

    return grouped_metrics

def compute_benchmark_metrics(results: dict) -> dict:
    """
    A partir de resultados brutos para distintos modelos, obtiene las métricas para todos ellos.
    """
    metrics = dict()

    for prompts_path in results.keys():
        prompts_results = results[prompts_path]
        prompts_metrics = dict()
        for model in prompts_results.keys():
            model_results = prompts_results[model]
            model_metrics = compute_metrics(model_results)
            prompts_metrics[model] = model_metrics
        metrics[prompts_path] = prompts_metrics
