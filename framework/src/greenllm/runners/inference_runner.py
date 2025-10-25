
import os, time, random
from typing import List
from ..emeter.nvml_meter import NvmlMeter
from ..emeter.codecarbon_meter import CodeCarbonMeter
from ..emeter.pyjoules_meter import PyJoulesMeter
from ..emeter.noop_meter import NoOpMeter
from ..carbon_feeds.generic import get_carbon_intensity

def _read_prompts(path) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    return lines

def _load_model(model_name: str, precision: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    kw = {}
    if precision == "int8":
        kw.update(dict(load_in_8bit=True, device_map="auto"))
    elif precision == "int4":
        try:
            kw.update(dict(load_in_4bit=True, device_map="auto"))
        except Exception:
            kw.update(dict(load_in_8bit=True, device_map="auto"))
    elif precision in ("fp16","bf16"):
        kw.update(dict(torch_dtype=torch.float16 if precision=="fp16" else torch.bfloat16, device_map="auto"))
    else:
        kw.update(dict(device_map="auto"))
    tok = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_name, **kw)
    return tok, model

def _generate_batch(tok, model, prompts, max_new_tokens=64):
    import torch
    batch = tok(prompts, return_tensors="pt", padding=True).to(model.device)
    with torch.no_grad():
        out = model.generate(**batch, max_new_tokens=max_new_tokens)
    texts = tok.batch_decode(out, skip_special_tokens=True)
    # Estimar tokens generados como diferencia
    print(texts)
    in_len = batch["input_ids"].shape[1]
    gen_tokens = 0
    for ids in out:
        gen_tokens += max(0, len(ids) - in_len)
    return texts, gen_tokens

def _get_meter(name: str):
    if name == "nvml":
        return NvmlMeter()
    if name == "codecarbon":
        return CodeCarbonMeter()
    if name == "pyjoules":
        return PyJoulesMeter()
    return NoOpMeter()

def run_measurement(model_name: str, prompts_path: str, max_new_tokens: int=64, batch_size:int=1,
                    precision:str="auto", meter_name:str="none", carbon_intensity: float=None, seed:int=42):
    random.seed(seed)
    prompts = _read_prompts(prompts_path)
    if not prompts:
        raise ValueError("No hay prompts en el archivo proporcionado.")
    meter = _get_meter(meter_name)
    tok, model = _load_model(model_name, precision)
    durations = []
    total_tokens = 0

    meter.start()
    t0 = time.time()
    # Procesar en lotes
    for i in range(0, len(prompts), batch_size):
        sub = prompts[i:i+batch_size]
        t1 = time.time()
        _, gen_toks = _generate_batch(tok, model, sub, max_new_tokens=max_new_tokens)
        dt = time.time() - t1
        durations.append(dt)
        total_tokens += int(gen_toks)
    m = meter.stop()

    energy_j = float(m.get("energy_j", 0.0))
    duration_s = float(m.get("duration_s", time.time()-t0))
    emissions_kg = m.get("emissions_kg", None)
    ci = get_carbon_intensity(carbon_intensity)

    return {
        "model": model_name,
        "precision": precision,
        "meter": meter_name,
        "prompts_count": len(prompts),
        "batch_size": batch_size,
        "max_new_tokens": max_new_tokens,
        "energy_j": energy_j,
        "duration_s_total": duration_s,
        "durations_s": durations,
        "tokens_generated": total_tokens,
        "emissions_kg": emissions_kg,
        "carbon_intensity_g_per_kwh": ci,
    }
