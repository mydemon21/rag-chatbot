import os
import requests
from typing import Dict, Any

class QrokLLMClient:
    def __init__(self):
        self.api_url = os.getenv("QROK_API_URL", "https://api.qrok.cloud/v1")
        self.api_key = os.getenv("QROK_API_KEY")
        
    def generate_response(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error generating response: {str(e)}"