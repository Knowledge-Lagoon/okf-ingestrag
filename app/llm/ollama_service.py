import requests


class OllamaService:

    def __init__(
        self,
        host="http://172.31.15.13:11434",
        model="phi3:mini"
    ):
        self.host = host
        self.model = model

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

        except Exception as ex:

            return f"ERROR: {str(ex)}"