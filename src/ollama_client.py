import requests
from .config import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaClient:
    def __init__(self, base_url=OLLAMA_BASE_URL, model=OLLAMA_MODEL):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def health(self):
        response = requests.get(f"{self.base_url}/api/tags", timeout=5)
        response.raise_for_status()
        models = [m.get("name", "") for m in response.json().get("models", [])]
        return models

    def generate(self, prompt):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False, "options": {"temperature": 0.1}},
            timeout=180,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
