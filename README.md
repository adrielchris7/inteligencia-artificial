# Curso de Inteligencia Artificial

Presentaciones y laboratorios de un curso de pregrado (AIMA / Russell & Norvig),
desde agentes y búsqueda hasta redes, refuerzo, visión, modelos de lenguaje,
RAG y GANs.

Cada unidad suele tener:

| Carpeta | Contenido |
|---|---|
| `PPTXs/` | Diapositivas 16:9 (español) |
| `project/` | Programas numerados (`01_*.py`, …), YAML editable, algoritmo a mano (sin NumPy / sklearn / Gym) |
| `Notebooks/` | Jupyter (Keras, FastText, Gemini, ChromaDB), cuando hay |
| `ejercicios/` o `Ejercicios/` | Tareas para el estudiante, cuando hay |
| `PDFs/`, `MDs/`, `HTMLs/` | Lecturas o notas, cuando hay |

## Laboratorios

En cada `project/`:

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python 01_*.py
```

Los detalles (qué imprime cada programa, qué editar en el YAML) están en el
`README.md` de esa unidad. La dependencia habitual es solo **PyYAML**.

No hace falta GPU: el laboratorio cabe en una tabla o en una matriz pequeña
que se puede calcular a mano.

## Unidades

Las presentaciones están en `Unidad/PPTXs/`. Los laboratorios, en `Unidad/project/`.

| Unidad | Presentación | Laboratorio | Ejercicios |
|---|---|---|---|
| [Conceptos básicos de IA](Conceptos%20Básicos%20de%20IA) | `estado-del-arte.pptx` | — | [01](Conceptos%20Básicos%20de%20IA/ejercicios/ejercicio-01.md) |
| [Agentes](Agentes) | `wumpus-world.pptx` | Wumpus (AIMA cap. 2) | [01](Agentes/ejercicios/ejercicio-01.md), [02](Agentes/ejercicios/ejercicio-02.md) |
| [Búsqueda no informada](Búsqueda%20no%20informada) | — | Rumania, BFS / UCS / DFS / DLS / IDS | [01](Búsqueda%20no%20informada/Ejercicios/ejercicio-01.md) |
| [Búsqueda informada](Búsqueda%20informada) | — | Rumania, voraz y A* | [01](Búsqueda%20informada/Ejercicios/ejercicio-01.md), [02](Búsqueda%20informada/Ejercicios/ejercicio-02.md) |
| [Razonamiento lógico](Razonamiento%20lógico) | `razonamiento-logico.pptx` | Encadenamiento hacia adelante / atrás | — |
| [Razonamiento probabilístico](Razonamiento%20probabilístico) | `redes-bayesianas.pptx` | Redes bayesianas | — |
| [Árboles de decisión](Árboles%20de%20decisión) | `arboles-de-decision.pptx` | ID3 | — |
| [Clustering K-medias](Clustering%20K-medias) | `clustering-k-medias.pptx` | Lloyd | [01](Clustering%20K-medias/Ejercicios/ejercicio-01.md) |
| [Perceptrón multicapa](Perceptrón%20multicapa) | PDFs (regresión, clasificación, redes) | MLP, XOR | [01](Perceptrón%20multicapa/Ejercicios/ejercicio-01.md) |
| [Cómputo evolutivo](Cómputo%20evolutivo) | `computo-evolutivo.pptx` | Algoritmo genético | — |
| [Q-learning](Q-learning) | `q-learning.pptx` | Q-learning tabular (pasillo A–B–G) | — |
| [Visión computacional](Visión%20computacional) | `vision-computacional.pptx` | Píxeles, convolución, Sobel | [01](Visión%20computacional/Ejercicios/ejercicio-01.md) |
| [GANs](GANs) | `gans.pptx` | Generador / discriminador 1D | — |
| [LLMs](LLMs) | `llms.pptx` | Siguiente token, softmax, atención | — |
| [RAG](RAG) | `RAG.pptx` | Embeddings, k-NN, citas | [Proyecto final](RAG/Proyecto%20final/proyecto%20RAG.md) |
| [AI Engineering](AI%20Engineering) | `the-ai-engineering-skills-map.pptx` | — | — |

GANs, LLMs y RAG incluyen diapositivas extra (embeddings, transformers, variantes
de GAN). Clustering, Perceptrón, Visión, LLMs y RAG tienen `Notebooks/`.

## Chatbot

Interfaz Streamlit que habla con **Gemini** (`gemini-3.6-flash`) o
**OpenAI** (`gpt-5.6-luna`, `gpt-4o-mini`). Elige proveedor y modelo en
la barra lateral. Necesita `GEMINI_API_KEY` de
[Google AI Studio](https://aistudio.google.com/apikey) y/o
`OPENAI_API_KEY` de [OpenAI](https://platform.openai.com/api-keys).

```bash
cd Chatbot
python3 -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cp .env.example .env              # pega tu clave; no lo subas a git
streamlit run app.py
```

Abre `http://localhost:8501`. Instrucciones completas en
[Chatbot/README.md](Chatbot/README.md).

## Otros materiales

| Carpeta | Qué es |
|---|---|
| [Mexico map](Mexico%20map) | Grafo de 1.000 ciudades de México; abre `mexico_map.html` en el navegador |
| [Git](Git) | [Instalación](Git/instalación.md) y [comandos](Git/comandos.md) |

## RAG del repositorio usando DeepWiki

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/victoruccetina/inteligencia-artificial)
