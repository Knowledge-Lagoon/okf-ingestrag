import os

import requests


class OllamaService:

    def __init__(
        self,
        host=None,
        model=None,
        connect_timeout=10,
        read_timeout=300,
    ):
        self.host = (
            host
            or os.getenv(
                "OLLAMA_HOST",
                "http://172.31.15.13:11434",
            )
        ).rstrip("/")

        self.model = (
            model
            or os.getenv(
                "OLLAMA_MODEL",
                "phi3:mini",
            )
        )

        self.timeout = (
            connect_timeout,
            read_timeout,
        )

    def ask(self, prompt):

        if not prompt or not prompt.strip():

            return (
                "ERROR: Prompt cannot be empty."
            )

        try:

            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "keep_alive": "10m",
                    "options": {
                        "num_predict": 180,
                        "temperature": 0.1,
                        "top_p": 0.9,
                    },
                },
                headers={
                    "Content-Type":
                        "application/json",
                },
                timeout=self.timeout,
            )

            response.raise_for_status()

            payload = response.json()

            answer = payload.get(
                "response",
                "",
            ).strip()

            if not answer:

                return (
                    "ERROR: Ollama returned "
                    "an empty response."
                )

            return answer

        except requests.exceptions.ReadTimeout:

            return (
                "ERROR: Ollama generation exceeded "
                f"{self.timeout[1]} seconds."
            )

        except requests.exceptions.ConnectTimeout:

            return (
                "ERROR: Connection to Ollama "
                "timed out."
            )

        except requests.exceptions.ConnectionError as ex:

            return (
                "ERROR: Could not connect to "
                f"Ollama: {ex}"
            )

        except requests.exceptions.HTTPError as ex:

            status_code = (
                ex.response.status_code
                if ex.response is not None
                else "unknown"
            )

            return (
                "ERROR: Ollama returned HTTP "
                f"{status_code}: {ex}"
            )

        except ValueError as ex:

            return (
                "ERROR: Ollama returned invalid "
                f"JSON: {ex}"
            )

        except Exception as ex:

            return (
                f"ERROR: {ex}"
            )