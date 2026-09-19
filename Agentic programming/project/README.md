# ReAct agent

A Reasoning + Acting loop you can read line by line (**no LangChain, no
LangGraph**): Gemini writes a Thought, optionally calls a tool, reads the
Observation, and repeats until a Final Answer. The default world is the
lecture example — packing for a trip, plus a calculator and a tiny
knowledge base.

The brain is Gemini (`google-genai`, same client as
`LLMs/Notebooks/04 LLM Gemini API.ipynb`). The loop (parse → tool →
observe → repeat) does not depend on that choice.

Paper: Yao et al., 2023, *ReAct: Synergizing Reasoning and Acting in
Language Models*.

## Setup

```bash
cd "Agentic programming/project"
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows (PowerShell):

```powershell
cd "Agentic programming/project"
python3 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and paste a Gemini key:

```
GEMINI_API_KEY=your_gemini_key_here
```

Get a key at [Google AI Studio](https://aistudio.google.com/apikey).
Do not commit `.env`. Optional: `GEMINI_MODEL` (default `gemini-3.6-flash`).

Later sessions: activate the venv again, then run the programs.
Deactivate with `deactivate`.

## Programs

Each program is one stage of the lecture.

| File | Stage |
|---|---|
| `01_show_tools.py` | Tools, YAML world, and the ReAct prompt |
| `02_one_step.py` | One Thought → Action → Observation cycle |
| `03_react_loop.py` | Full loop until Final Answer (or `max_steps`) |
| `04_compare.py` | CoT with no tools vs ReAct with tools |

```bash
python 01_show_tools.py
python 02_one_step.py
python 02_one_step.py --all
python 03_react_loop.py
python 03_react_loop.py --all
python 03_react_loop.py --query "¿Qué ropa me conviene llevar a Cancún?"
python 04_compare.py --all
```

All four default to `data/viaje.yaml`. Override with `--data`, `--query`,
`--max-steps`, or `--all`. Without `--query`, programs 02–04 run the first
YAML query (`--all` runs every one).

## The four stages

1. **Tools** (`react/tools.py`, `react/prompt.py`) — Calculator, Lookup, and
   Weather, plus the canonical ReAct prompt that lists them.
2. **One step** (`react/parse.py`) — Gemini writes Thought + Action +
   Action Input; the environment returns Observation.
3. **Loop** (`react/loop.py`) — after each observation, either another
   cycle or `Final Answer`. `max_steps` stops infinite loops.
4. **Compare** (`react/brain.py`) — the same questions without tools
   (Gemini answers from its own knowledge) and with tools (grounded in
   the YAML world).

## Edit the world

Open `data/viaje.yaml` (or copy it).

```yaml
name: Empacar y calcular
max_steps: 6

facts:
  - key: closet
    aliases: [closet, armario, ropa]
    text: En el closet hay un suéter de lana, una chamarra, shorts y una playera ligera.

weather:
  Monterrey:
    temp: 8
    summary: frío y viento

queries:
  - ¿Qué ropa me conviene llevar a Monterrey?
```

- `facts` feed **Lookup**. `aliases` are extra keys the tool will match.
- `weather` feeds **Weather**. City names in a question select the forecast.
- Arithmetic questions go to **Calculator** (`17 * 24 + 5`, no `eval()`).

## What to expect

**`01_show_tools.py`** — three tools and the prompt with
`Action: the action to take, should be one of [Calculator, Lookup, Weather]`.

**`02_one_step.py`** — packing for Monterrey usually starts with Weather.
It does not look in the closet yet.

**`03_react_loop.py`** — the packing question typically does two tool
calls, then stops: Weather → Lookup `closet` → Final Answer (suéter and
chamarra, not shorts). `17 * 24 + 5` is **413**. The ReAct paper question
looks up the Yao et al., 2023 fact. Exact wording varies with Gemini.

**`04_compare.py`** — without tools Gemini answers from parametric
knowledge (it does not see the closet or the YAML forecast). With tools
those answers are grounded by Weather, Calculator, and Lookup.

A production ReAct agent is this loop at scale: the same Thought / Action /
Observation text, with an LLM writing each turn and real APIs behind
the tools.
