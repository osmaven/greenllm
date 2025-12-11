import requests
import json
import re
import time

with open("../api.key", "r") as f:
    API_KEY = f.read().strip()

# Endpoint para generación de contenido
# IMPORTANTE: sustituye el modelo en el payload, no en la URL
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key=" + API_KEY


def evaluar_modelos(prompts, disciplinas, resultados, seed, model="gemini-2.5-flash-lite"):
    """
    Evalúa resultados generados por modelos usando Google Gemini.
    Devuelve una lista con puntajes (0.0 a 10.0).
    """

    puntuaciones = []

    headers = {
        "Content-Type": "application/json"
    }

    for i, (prompt_text, disciplina_text, resultado_text) in enumerate(zip(prompts, disciplinas, resultados), start=1):

        time.sleep(5)

        prompt = f"""
        You are an expert evaluator of language model outputs.

        Your task is to assign a single decimal score between 0 and 10 
        for the overall quality of the following model-generated result.

        The score should be based on:
        - Clarity and coherence of the response
        - Relevance to the prompt
        - Accuracy or factual correctness (if applicable)
        - Appropriateness to the context of the discipline: {disciplina_text}
        - Ignore any extra commentary in the response; focus only on whether the answer is correct or relevant.

        Return ONLY the number (e.g., 7.8). 
        Do not include any extra text, labels, or explanations.
        If there is no answer or is non-sense, return 0.0.
        Consider that are very small models with bad performance.
        Ignore extra commentary in the response; focus only on whether the answer is correct or relevant.
        ---
        Original prompt:
        {prompt_text}

        Response to evaluate:
        {resultado_text}
        ---
        """

        # Gemini usa estructura "contents" → "parts" → "text"
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "seed": seed
            }
        }

        # Construir la URL específica del modelo
        url = API_URL.format(model=model)

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)

            if response.status_code == 200:
                result = response.json()

                # Extraer texto devuelto por Gemini
                contenido = (
                    result.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "")
                    .strip()
                )

                print(contenido)
                # Limpiar y extraer número
                contenido_limpio = re.sub(r"<.*?>", "", contenido, flags=re.DOTALL).strip()
                match = re.search(r"\b\d+(\.\d+)?\b", contenido_limpio)

                if match:
                    puntuacion = float(match.group(0))
                    puntuacion = max(0.0, min(10.0, puntuacion))
                else:
                    print(f"[Warning] No se pudo extraer valor numérico en prompt {i}. Valor asignado: 0.0")
                    puntuacion = 0.0

            else:
                print(f"[HTTP Error {response.status_code}] {response.text}")
                puntuacion = 0.0

        except Exception as e:
            print(f"[Error] Procesando prompt {i}: {e}")
            puntuacion = 0.0

        puntuaciones.append(puntuacion)

    return puntuaciones
