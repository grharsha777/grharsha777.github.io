import os
import requests
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
print(f"Testing with API Key ending in: ...{MISTRAL_API_KEY[-4:] if MISTRAL_API_KEY else 'None'}")

headers = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "mistral-tiny",
    "messages": [
        {"role": "user", "content": "Say hello!"}
    ],
    "max_tokens": 10
}

try:
    response = requests.post("https://api.mistral.ai/v1/chat/completions", json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
