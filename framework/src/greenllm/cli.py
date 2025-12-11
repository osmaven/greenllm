import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from transformers import logging as hf_logging
hf_logging.set_verbosity_error()


import argparse, json, time, os
from .metrics.metrics import compute_metrics
from .exporters.json_exporter import JSONExporter

from .login.login import login_hugging_face
import shutil
import datetime


def main():

    parser = argparse.ArgumentParser(prog="greenllm", description="Medición energética/CO2e para LLM (docente)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("measure", help="Ejecuta inferencia y mide energía/métricas")
    m.add_argument("--model", required=True, help="Nombre del modelo HF")
    m.add_argument("--prompts", required=True, help="Ruta a archivo de prompts (uno por línea)]")

    m.add_argument("--max-new-tokens", type=int, default=64)

    m.add_argument("--batch-size", type=int, default=1)
    m.add_argument("--precision", choices=["fp16","bf16","int8","int4","auto"], default="auto")

    m.add_argument("--meter", choices=["codecarbon"], default="codecarbon")

    m.add_argument("--carbon-intensity", default= 'auto', help="gCO2e/kWh (si no se usa fuente externa)")

    m.add_argument("--json", default=None, help="Ruta de salida JSON")
    
    m.add_argument("--seed", type=int, default=42)
    m.add_argument("--n-iterations", type=int, default=1, help="Número de iteraciones sobre el conjunto de prompts")

    m.add_argument("--verbose", type = bool, default = False, help="Modo verbose")

    args = parser.parse_args()

    print("""\033[32m 
                            _ _           
   __ _ _ __ ___  ___ _ __ | | |_ __ ___  
  / _` | '__/ _ \/ _ \ '_ \| | | '_ ` _ \ 
 | (_| | | |  __/  __/ | | | | | | | | | |
  \__, |_|  \___|\___|_| |_|_|_|_| |_| |_|
  |___/                                   \n""")
    


    columnas = shutil.get_terminal_size().columns
    print("-" * columnas)
    print(f'[greenllm @ {datetime.datetime.now().strftime("%H:%M:%S")}] \033[0m Ejecutando medición con los siguientes parámetros: \nModelo: {args.model}\nPrompts: {args.prompts}\nMax new tokens: {args.max_new_tokens}\nBatch size: {args.batch_size}\nPrecision: {args.precision}\nMedidor: {args.meter}\nCarbon intensity: {args.carbon_intensity}\nSeed: {args.seed}\nIteraciones: {args.n_iterations}\n', "\033[0m")

    login_hugging_face()

    from .runners.inference_runner import run_measurement
    results = run_measurement(
        model_name=args.model,
        prompts_path=args.prompts,
        max_new_tokens=args.max_new_tokens,
        batch_size=args.batch_size,
        precision=args.precision,
        meter_name=args.meter,
        carbon_intensity=args.carbon_intensity,
        seed=args.seed,
        n_iterations=args.n_iterations,
        verbose= args.verbose
    )
    

    # Derivar métricas agregadas
    metrics = compute_metrics(results)
    print(json.dumps(metrics, indent=2))

    if args.json:
        JSONExporter(args.json).export(metrics)
        print(f"[greenllm] JSON escrito en: {args.json}")




