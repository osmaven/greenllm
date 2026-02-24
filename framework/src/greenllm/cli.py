
import argparse, json, time, os
from .runners.inference_runner import run_measurement
from .metrics.metrics import compute_metrics
from .exporters.csv_exporter import CSVExporter
from .exporters.mlflow_exporter import MLflowExporter
from .users.invite import generate_invitation, load_invitations

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

    # invite subcommand
    inv = sub.add_parser("invite", help="Invita a un nuevo usuario a la plataforma")
    inv.add_argument("--email", required=True, help="Correo electrónico del usuario a invitar")
    inv.add_argument("--role", default="student", choices=["student", "instructor", "admin"],
                     help="Rol asignado al usuario (por defecto: student)")
    inv.add_argument("--store", default=None, help="Ruta del fichero JSON donde se almacenan las invitaciones")

    args = parser.parse_args()

    if args.cmd == "invite":
        kwargs = {"email": args.email, "role": args.role}
        if args.store:
            kwargs["store_path"] = args.store
        invitation = generate_invitation(**kwargs)
        print(json.dumps(invitation, indent=2))
        return

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
