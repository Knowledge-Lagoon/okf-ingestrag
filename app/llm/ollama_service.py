import os
import ollama


class OllamaService:

    def __init__(
        self,
        model: str | None = None,
        host: str | None = None
    ):
        self.model = model or os.getenv(
            "OLLAMA_MODEL",
            "phi3:mini"
        )

        self.host = host or os.getenv(
            "OLLAMA_HOST",
            "http://172.31.15.13:11434"
        )

        self.client = ollama.Client(
            host=self.host
        )

    def ask(self, prompt: str) -> str:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]