# Deployment Notes

## Primary Target: Streamlit Community Cloud

### Why
- Free tier with generous limits
- Direct GitHub repo connection — push to `main` triggers auto-deploy
- Built-in secrets management (no `.env` file on server)
- No Docker or Dockerfile needed
- Public URL for demo sharing

### Setup Steps

1. **Push code to GitHub** (public repo)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select the repo: `<your-username>/sdc2-copilot`
5. Set the main file path: `app/streamlit_app.py`
6. Set Python version: `3.12`
7. Add secrets in the Streamlit Cloud dashboard:
   - `GEMINI_API_KEY`
   - `GROQ_API_KEY`
   - `LLM_PROVIDER` (default: `gemini`)
8. Deploy

### Secrets Configuration

In the Streamlit Cloud dashboard, add secrets in TOML format:

```toml
GEMINI_API_KEY = "your-gemini-api-key"
GROQ_API_KEY = "your-groq-api-key"
LLM_PROVIDER = "gemini"
```

These are accessible in the app via `st.secrets` or `os.environ`.

### Requirements

Streamlit Cloud reads `requirements.txt` from the repo root. No `setup.py` or `pyproject.toml` needed.

### Python Version

Create a `.python-version` file in the repo root if needed:
```
3.12
```

---

## Alternative Targets (Post-MVP)

### Hugging Face Spaces
- Requires a `Dockerfile` or `app.py` at root
- Supports Streamlit natively with `sdk: streamlit` in `README.md` YAML
- Free tier available

### Render
- Requires a `Dockerfile` or `render.yaml`
- Supports web service deployment
- Persistent disk available
- Custom domains supported

---

## Local Development

```bash
# Always activate venv first
.\.venv\Scripts\Activate.ps1

# Run the app
streamlit run app/streamlit_app.py

# Run tests
pytest tests/ -v
```

The app works fully offline using the `template` LLM provider (no API key needed).
