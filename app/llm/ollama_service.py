# app/llm/ollama_service.py

import requests


class OllamaService:

    def __init__(
        self,
        host="http://172.31.15.13:11434",
        model="phi3:mini"
    ):
        self.host = host
        self.model = model

    def ask(self, prompt: str):

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            f"{self.host}/api/generate",
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        return response.json()["response"]