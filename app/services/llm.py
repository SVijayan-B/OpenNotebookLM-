import requests
from typing import Optional


class OllamaLLM:
    def __init__(
        self,
        model: str = "mistral:7b-instruct-q4_K_M",
        base_url: str = "http://localhost:11434",
        timeout: int = 120,
    ):
        self.model = model
        self.url = f"{base_url}/api/generate"
        self.timeout = timeout

    def generate(
        self,
        question: str,
        context: str,
    ) -> Optional[str]:
        """
        Generates an answer strictly from provided context.
        """

        if not context.strip():
            return None

        prompt = f"""
You are a research assistant.

RULES:
- Answer ONLY using the provided context.
- If the answer is not contained in the context, say:
  "I don't know based on the provided documents."
- Do NOT use prior knowledge.
- Be concise and factual.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
""".strip()

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(
            self.url,
            json=payload,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json().get("response", "").strip()
