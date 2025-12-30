from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import requests

# Load environment variables from .env file (for local dev)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, use system env vars

# Add the current directory to sys.path to ensure module imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag_engine import PortfolioRAG

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Configuration - Load from environment variables
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_MODEL = "mistral-tiny" 

# Initialize RAG Engine
try:
    rag = PortfolioRAG()
except Exception as e:
    print(f"Failed to initialize RAG Engine: {e}")
    rag = None

SYSTEM_PROMPT = """
You are an AI portfolio assistant for G R Harsha. 
Use the provided CONTEXT to answer the user's question. 
If the answer is not in the context, say "I don't have that specific information in my knowledge base yet, but I can tell you about Harsha's projects, skills, and experience."
Do not hallucinate or make up facts.
Keep answers professional, concise (under 3 sentences if possible), and engaging.
You are talking to recruiters or potential collaborators.

IMPORTANT FORMATTING RULES:
- When mentioning URLs or links, ALWAYS format them as HTML hyperlinks: <a href="URL" target="_blank">Link Text</a>
- For GitHub repos, format as: <a href="https://github.com/grharsha777/REPO_NAME" target="_blank">Repo Name</a>
- For LinkedIn, format as: <a href="https://www.linkedin.com/in/grharsha777/" target="_blank">LinkedIn Profile</a>
- For Resume, format as: <a href="https://drive.google.com/file/d/1BnObISeyCMV9UTi9V_qIKWJitsyrycq1/view" target="_blank">View Resume</a>
- Make links clickable and professional.

IMPORTANT DATA RULES:
- If the context contains "[CRITICAL DATA]" regarding GitHub statistics, use THAT number for the total repositories. 
- Do NOT count the projects in the "Projects" section to determine the total repository count; rely ONLY on the GitHub Statistics section for the total number.
"""

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400
    
    user_query = data["message"]
    
    if not rag:
         return jsonify({"response": "System is initializing or in error state. Please check server logs."}), 500

    # 1. Retrieve Context
    try:
        context = rag.query(user_query)
    except Exception as e:
        print(f"RAG Error: {e}")
        context = "Error retrieving context."
    
    # 2. Construct Prompt for Mistral
    prompt = f"{SYSTEM_PROMPT}\n\nCONTEXT:\n{context}\n\nUSER QUESTION:\n{user_query}\n\nANSWER:"
    
    # 3. Call Mistral API
    try:
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mistral-tiny", # or mistral-small, mistral-medium
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300
        }
        
        response = requests.post("https://api.mistral.ai/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        
        return jsonify({"response": ai_response})
        
    except Exception as e:
        print(f"Error calling AI: {e}")
        return jsonify({"response": "I'm having trouble connecting to my brain right now. Please try again later."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
