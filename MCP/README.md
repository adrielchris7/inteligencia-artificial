# MCP (FastMCP)

Servidor MCP mínimo con [FastMCP](https://gofastmcp.com): dos tools, un
resource y un prompt. MCP (Model Context Protocol) es el protocolo con el
que un cliente (Cursor, Claude Desktop, u otro agente) descubre y llama
funciones de un proceso aparte.

Necesitas **Python 3.10 o superior**. FastMCP no instala en 3.9.

## Setup

```bash
cd MCP
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows (PowerShell):

```powershell
cd MCP
python3 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Later sessions: activate the venv again, then run the programs.
Deactivate with `deactivate`.

## Programs

| File | Role |
|---|---|
| `server.py` | Servidor MCP (stdio por defecto) |
| `client.py` | Cliente in-process: lista tools y llama `greet` / `add` |

```bash
python client.py
python server.py
fastmcp run server.py --transport http --port 8000
```

`python server.py` se queda esperando en stdin/stdout: así lo arrancan
Cursor y Claude Desktop. Para ver las tools sin un host MCP, usa
`python client.py`.

## What to expect

**`python client.py`** — imprime `greet`, `add`, el texto del resource
`info://server`, y el prompt `explain` con el tema MCP.

**`python server.py`** — no imprime un menú. El cliente MCP habla con él
por stdio.

**HTTP** — `fastmcp run server.py --transport http --port 8000` deja el
endpoint en `http://localhost:8000/mcp`.

## Cursor

El archivo del repo es [`.cursor/mcp.json`](../.cursor/mcp.json). Cursor lo
lee al abrir este workspace. Si prefieres el servidor en todos tus
proyectos, copia el mismo bloque a `~/.cursor/mcp.json` con rutas
absolutas.

En Cursor: **Settings → Cursor Settings → MCP**. Activa `demo`. En el
chat de Agent deberías ver las tools `greet` y `add`.
