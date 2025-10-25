
import argparse, json, time, os
from .runners.inference_runner import run_measurement
from .metrics.metrics import compute_metrics
from .exporters.csv_exporter import CSVExporter
from .exporters.mlflow_exporter import MLflowExporter

def main():
    parser = argparse.ArgumentParser(prog="greenllm", description="Medición energética/CO2e para LLM (docente)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("measure", help="Ejecuta inferencia y mide energía/métricas")
    m.add_argument("--model", required=True, help="Nombre del modelo HF")
    m.add_argument("--prompts", required=True, help="Ruta a archivo de prompts (uno por línea)")
    m.add_argument("--max-new-tokens", type=int, default=64)
    m.add_argument("--batch-size", type=int, default=1)
    m.add_argument("--precision", choices=["fp16","bf16","int8","int4","auto"], default="auto")
    m.add_argument("--meter", choices=["nvml","codecarbon","pyjoules","none"], default="none")
    m.add_argument("--carbon-intensity", type=float, default=None, help="gCO2e/kWh (si no se usa fuente externa)")
    m.add_argument("--csv", default=None, help="Ruta de salida CSV")
    m.add_argument("--mlflow-uri", default=None, help="MLflow tracking URI")
    m.add_argument("--experiment", default="greenllm", help="Nombre de experimento MLflow")
    m.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    results = run_measurement(
        model_name=args.model,
        prompts_path=args.prompts,
        max_new_tokens=args.max_new_tokens,
        batch_size=args.batch_size,
        precision=args.precision,
        meter_name=args.meter,
        carbon_intensity=args.carbon_intensity,
        seed=args.seed,
    )

    # Derivar métricas agregadas
    metrics = compute_metrics(results)
    payload = {**results, **metrics}
    print(json.dumps(payload, indent=2))

    # Exportadores opcionales
    if args.csv:
        CSVExporter(args.csv).export(payload)
        print(f"[greenllm] CSV escrito en: {args.csv}")

    if args.mlflow_uri:
        MLflowExporter(experiment=args.experiment, tracking_uri=args.mlflow_uri).export(payload)
        print(f"[greenllm] Registro en MLflow ({args.mlflow_uri}).")
