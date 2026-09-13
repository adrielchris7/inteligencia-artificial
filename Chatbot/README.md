# Chatbot

A Streamlit chat UI that talks to **Gemini** or **OpenAI**. Pick the
provider and model in the sidebar. Gemini uses the same client as
`LLMs/Notebooks/04 LLM Gemini API.ipynb`: `google-genai` and
`gemini-3.6-flash`. OpenAI uses the official `openai` SDK
(`gpt-5.6-luna` or `gpt-4o-mini`).

## Setup

```bash
cd Chatbot
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows (PowerShell):

```powershell
cd Chatbot
python3 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and paste the key for the provider you
want to use (you can put both):

```
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
```

- Gemini: [Google AI Studio](https://aistudio.google.com/apikey)
- OpenAI: [OpenAI API keys](https://platform.openai.com/api-keys)

Do not commit `.env`. Later sessions: activate the venv again, then run
the app. Deactivate with `deactivate`.

If Gemini returns **403 / leaked**, that key is already public (for
example committed in git). Google will not accept it again: create a
fresh key, revoke the old one in AI Studio, and put only the new key in
`.env`.

## Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`. Choose **Proveedor** and
**Modelo** in the sidebar, then type in the chat box. Conversation
history stays in the session; changing model starts a new chat.
**Nuevo chat** also starts over. Stop the server with `Ctrl+C`.
