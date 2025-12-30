# G R Harsha - Portfolio RAG Chatbot

This repository contains the source code for my portfolio website and a context-aware AI chatbot built using **Mistral AI** and **Retrieval-Augmented Generation (RAG)**.

## Architecture

- **Frontend**: HTML/CSS/JS (Static site)
- **Backend**: Flask API (Python)
- **Vector Database**: ChromaDB
- **LLM**: Mistral AI (`mistral-tiny`)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Live Integrations**: GitHub API (for repos/stats), LinkedIn (profile data)

## Backend Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory (use `.env.example` as a template):
```env
MISTRAL_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
LINKEDIN_CLIENT_ID=your_id_here
LINKEDIN_CLIENT_SECRET=your_secret_here
```

### 3. Run the Backend
```bash
python backend/server.py
```
The server will start at `http://localhost:8000`.

## Frontend Integration

The chatbot UI in `js/chatbot.js` is configured to connect to `http://localhost:8000/chat`. 

### Deployment Note
- **Frontend**: Deployed to GitHub Pages.
- **Backend**: Needs to be hosted on a platform that supports Python (e.g., Render, Railway, or VPS). Update the API URL in `js/chatbot.js` once the backend is deployed.

## Security
All API keys and secrets are managed via environment variables and are excluded from version control via `.gitignore`.
