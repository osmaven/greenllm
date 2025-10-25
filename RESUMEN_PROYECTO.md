# Resumen del Proyecto: Curso de Algoritmos Sostenibles para LLM

A continuación, se presenta un resumen completo del contenido y los componentes del proyecto "Curso de Algoritmos Sostenibles para LLM".

## 1. Visión General del Proyecto

El repositorio contiene todos los materiales para un curso universitario enfocado en la **sostenibilidad y eficiencia de los Modelos de Lenguaje Grandes (LLM)**. Su objetivo es proporcionar a los estudiantes tanto el marco teórico como las herramientas prácticas para medir, analizar y optimizar el impacto energético y la huella de carbono de estos modelos.

## 2. Componentes Principales

El proyecto se estructura en torno a varios directorios clave:

*   **`framework/` - El Framework `greenllm`:**
    *   Es el corazón del proyecto. Se trata de un paquete de Python (`greenllm`) diseñado específicamente para **medir la eficiencia de los LLMs**.
    *   **Funcionalidades clave:**
        *   **Medición de energía:** Se integra con herramientas como NVIDIA NVML, CodeCarbon y PyJoules para medir el consumo energético durante la inferencia.
        *   **Cálculo de métricas:** A partir de los datos brutos, calcula métricas de sostenibilidad como Joules por token, tokens por Joule y emisiones de CO₂e.
        *   **Exportación de resultados:** Permite guardar los resultados de los experimentos en formatos como CSV o registrarlos en MLflow para un seguimiento avanzado.
    *   Su diseño es modular y prioriza la claridad del código, ya que su propósito es principalmente docente.

*   **`docs/` - Documentación del Curso:**
    *   Contiene todos los documentos académicos esenciales, como el **sílabo (`SYLLABUS.md`)**, los **requisitos técnicos (`REQUISITOS.md`)**, las **rúbricas de evaluación (`RUBRICAS.md`)** y la **bibliografía (`BIBLIOGRAFIA.md`)**.

*   **`asignaciones/` - Retos Prácticos:**
    *   Define tres retos progresivos que guían a los estudiantes en la aplicación práctica de los conceptos:
        *   **Reto 1:** Definición y medición de métricas de sostenibilidad.
        *   **Reto 2:** Extensión del framework `greenllm` (por ejemplo, añadiendo nuevos medidores).
        *   **Reto 3:** Optimización de un modelo (mediante cuantización, destilación, etc.) y análisis comparativo del antes y el después.

*   **`website/` - Visualizador Web de la Documentación:**
    *   Recientemente, se ha añadido una **página web estática** que renderiza todos los archivos Markdown del proyecto.
    *   Permite a los usuarios navegar por el sílabo, los retos y demás documentos de forma cómoda desde un navegador, sin necesidad de configurar un servidor. Se basa en un script (`build.py`) que convierte los `.md` a `.html`.

## 3. Recursos de Apoyo

*   **`notebooks/`:** Incluye plantillas de Jupyter Notebooks para que los estudiantes realicen y documenten sus experimentos.
*   **`scripts/` y `data/`:** Proporcionan scripts de ejemplo para ejecutar benchmarks y un conjunto de datos con prompts para realizar pruebas estandarizadas.

En resumen, el proyecto es un ecosistema educativo completo que combina teoría, documentación y una herramienta de software funcional para capacitar a los estudiantes en el campo emergente de la IA sostenible.
