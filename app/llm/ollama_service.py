import requests


class OllamaService:

    ...

    def ask(self, prompt):

        try:

            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()

            return response.json()["response"]

        except requests.exceptions.ReadTimeout:

            return (
                "ERROR: Ollama request timed out. "
                "Check model availability or reduce prompt size."
            )