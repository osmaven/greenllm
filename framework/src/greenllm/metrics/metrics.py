
def compute_metrics(results: dict) -> dict:
    """
    A partir de resultados brutos (energía J, tokens, latencias), devuelve métricas derivadas.
    Espera claves: energy_j, tokens_generated, durations_s (lista), emissions_kg opcional, carbon_intensity_g_per_kwh opcional.
    """
    energy_j = float(results.get("energy_j", 0.0))
    tokens = int(results.get("tokens_generated", 0))
    durations = results.get("durations_s", [])
    co2e_g = None

    # Energía y tokens
    j_per_token = (energy_j / tokens) if tokens > 0 else None
    tokens_per_j = (tokens / energy_j) if energy_j > 0 else None

    # CO2e estimado (si hay intensidad y/o emissions_kg de CodeCarbon)
    if "emissions_kg" in results and results["emissions_kg"] is not None:
        co2e_g = results["emissions_kg"] * 1000.0
    else:
        # Si tenemos intensidad (g/kWh), pasar energía J -> kWh = J / 3.6e6
        I = results.get("carbon_intensity_g_per_kwh", None)
        if I is not None:
            co2e_g = (energy_j / 3_600_000.0) * float(I)

    # Percentiles de latencia simples
    def perc(xs, p):
        if not xs: return None
        xs2 = sorted(xs)
        k = int((len(xs2)-1) * p)
        return xs2[k]

    p50 = perc(durations, 0.50)
    p95 = perc(durations, 0.95) if len(durations) > 1 else p50

    # Normalización por 1k tokens
    co2e_per_1k = (co2e_g / (tokens/1000)) if (co2e_g is not None and tokens > 0) else None

    return {
        "j_per_token": j_per_token,
        "tokens_per_joule": tokens_per_j,
        "latency_p50_s": p50,
        "latency_p95_s": p95,
        "co2e_g_total": co2e_g,
        "co2e_g_per_1k_tokens": co2e_per_1k,
    }
