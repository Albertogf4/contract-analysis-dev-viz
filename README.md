# Análisis de contratos
Facilitar la búsqueda trazable y la extracción estructurada de campos esenciales en contratos, ofreciendo una interfaz sencilla con referencias al PDF.


## Objetivos

- Desarrollo del pipeline de ingesta + parsing + chunking por secciones.
- Extracción y generación de un modelo de datos estructurado (grafos) a partir de un contrato
- Creación de base de conocimiento (grafo + vectorizada)
- Generación de un sistema RAG 
- Ajuste de modelo de embeddings para aumento de precisión en el dominio financiero
- Interfaz chat al asistente contractual e interfaz de visualización de resultados
- (secundario) Reranker de chunks

## Plan 

### Fase 0 — Setup & entrenamiento modelo(semana 1-2)
- Crear repositorio y estructura (`backend/`, `frontend/`, `data/`, `eval/`).
- Definir esquema mínimo de datos y **Pydantic models** para las entidades a extraer.
- Preparar un pequeño dataset de prueba.
- Elección modelos baseline
- Evaluar modelos de embeddings, entrenar adaptors

### Fase 1 — Ingesta y búsqueda (semanas 3–4)
- Conversión de PDF a texto con **chunking por índice**.
- Implementación de embeddings baseline.
- Desarrollo de un endpoint de búsqueda con **citas** (página + fragmento).
- Métricas iniciales de retrieval.

### Fase 2 — Extracción mínima (semanas 5-6)
- Uso de prompts con salida **JSON estricta** (Pydantic).
- Extracción de campos.
- Validaciones y enlaces a **spans del PDF**.

### Fase 3 — Grafo y visualización (semanas 7-8)
- Construcción de un **grafo**.
- Desarrollo de un **dashboard** con buscador, tabla de campos y vista de grafo básica (zoom/pan).

### Fase 4 — Evaluación y entrega (semanas 9-10)
- Evaluación de métricas de extracción por campo (precisión/recobrado en dataset pequeño).
- Preparación de la **demo y documentación** final.
