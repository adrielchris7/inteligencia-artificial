# Diagrama del agente ReAct

El agente es un ciclo **Thought → Action → Observation** hasta un **Final Answer** o hasta `max_steps`. Gemini solo escribe el razonamiento y la acción; el entorno ejecuta la tool y devuelve la observación.

```mermaid
flowchart TD
    start(["Pregunta + mundo YAML + tools"]) --> prompt["build_prompt<br/>lista Calculator, Lookup, Weather<br/>y el formato ReAct"]
    prompt --> loop{"¿quedan pasos<br/>en max_steps?"}

    loop -->|"no"| cap["Trace.stopped = max_steps"]
    loop -->|"sí"| gemini["GeminiBrain.next_action<br/>prompt + pasos previos<br/>para antes de Observation"]

    gemini --> parse["parse<br/>texto libre → Decision"]

    parse --> kind{"¿Final Answer<br/>o Action?"}

    kind -->|"Thought + Final Answer<br/>decision.done"| done["append Step<br/>Trace.stopped = final"]
    kind -->|"Thought + Action<br/>+ Action Input"| tool["run_tool"]

    tool --> calc["Calculator<br/>aritmética por AST"]
    tool --> look["Lookup<br/>hechos del YAML"]
    tool --> weather["Weather<br/>pronóstico del YAML"]
    tool --> unk["tool desconocida<br/>mensaje de error"]

    calc --> obs["Observation"]
    look --> obs
    weather --> obs
    unk --> obs

    obs --> append["append Step al Trace"]
    append -->|"el siguiente Thought<br/>ya ve esta Observation"| loop

    done --> answer(["Trace.answer"])
    cap --> answer
```

Piezas que corresponden al código:

- **`run_react`** en `react/loop.py` arma el prompt, pide un turno, parsea y decide si parar o llamar una tool.
- **`GeminiBrain`** en `react/brain.py` genera un solo turno y se detiene en `Observation:`, para no inventar el resultado.
- **`parse`** en `react/parse.py` acepta `Thought + Final Answer` o `Thought + Action + Action Input`. Si aparecen ambos, gana Final Answer salvo que el Thought ya traiga un `Action:`.
- **`run_tool`** en `react/tools.py` no usa APIs reales: Calculator evalúa la expresión, Lookup y Weather leen `data/viaje.yaml`.
