import requests

OLLAMA_HOST = "http://13.210.36.161:11434"   # replace with your IP

payload = {
    "model": "phi3",
    "prompt": "What is Kubernetes?",
    "stream": False
}

response = requests.post(
    f"{OLLAMA_HOST}/api/generate",
    json=payload,
    timeout=120
)

print(response.status_code)
print(response.text)
