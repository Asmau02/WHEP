# WHEP
## Women's Health Education Platform

WHEP is an educational RAG application. It retrieves relevant passages from a curated ChromaDB knowledge base and uses Groq to generate a grounded response.

### Project structure

- `app.py`: Streamlit interface
- `whep/retrieval.py`: ChromaDB retrieval
- `whep/generation.py`: Groq response generation
- `whep/config.py`: API-key configuration
- `chroma_db_v2/`: place the existing ChromaDB persistence directory here

### Before running

1. Copy the existing `chroma_db_v2` directory into this project folder. It must contain the persisted ChromaDB files, not just a placeholder.
2. Confirm the collection name is `whep_health_sources_clean`.
3. Create `.streamlit/secrets.toml` by copying `.streamlit/secrets.toml.example`.
4. Put your NEW Groq API key in `secrets.toml`. Never upload that file to GitHub.

### Run locally

Install Python, then open a terminal in this project folder and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Important note about GitHub

Do not commit API keys. Also check the size of `chroma_db_v2` before uploading it. GitHub blocks ordinary files larger than 100 MB and recommends keeping repositories small. If the database is large, we should store it separately and configure the deployed app to retrieve it securely.

### Health and safety

WHEP is for general health education. It is not a substitute for professional medical assessment, diagnosis, or treatment. The knowledge base and generated answers require ongoing clinical and editorial review before public use.
