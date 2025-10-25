
class MLflowExporter:
    def __init__(self, experiment="greenllm", tracking_uri=None):
        self.experiment = experiment
        self.tracking_uri = tracking_uri

    def export(self, payload: dict):
        try:
            import mlflow
            if self.tracking_uri:
                mlflow.set_tracking_uri(self.tracking_uri)
            mlflow.set_experiment(self.experiment)
            with mlflow.start_run():
                # Log parámetros y métricas clave
                params = {k: v for k, v in payload.items() if isinstance(v, (str, int, float))}
                mlflow.log_params(params)
                # Métricas (si existen)
                for k in ["j_per_token","tokens_per_joule","latency_p50_s","latency_p95_s","co2e_g_total","co2e_g_per_1k_tokens"]:
                    if k in payload and payload[k] is not None:
                        mlflow.log_metric(k, float(payload[k]))
        except Exception as e:
            print(f"[MLflowExporter] MLflow no disponible o error: {e}")
