import requests


class OllamaService:

    def __init__(
        self,
        host="http://13.210.36.161:11434",
        model="phi3"
    ):
        self.host = host
        self.model = model

    def generate(self, prompt: str):

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