import json
from typing import Any

from chartspeak.backends.base import Backend
from chartspeak.errors import BackendError

_DEFAULT_MODEL = "qwen2.5:3b"
_DEFAULT_URL = "http://localhost:11434"


class OllamaBackend(Backend):
    """Backend using a locally running Ollama instance."""

    def __init__(self, model: str = _DEFAULT_MODEL, base_url: str = _DEFAULT_URL) -> None:
        self.model = model
        self.base_url = base_url

    def spec(self, system: str, user: str, json_schema: dict[str, Any]) -> str:
        try:
            import ollama  # noqa: PLC0415
        except ImportError as e:
            raise BackendError(
                "ollama package not installed. Run: pip install chartspeak[ollama]"
            ) from e

        try:
            client = ollama.Client(host=self.base_url)
            response = client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                format=json_schema,
                options={"temperature": 0},
            )
        except Exception as e:
            raise BackendError(
                f"Ollama request failed: {e}\nMake sure Ollama is running: https://ollama.com"
            ) from e

        content = response.message.content
        if not content:
            raise BackendError("Ollama returned an empty response.")
        return content if isinstance(content, str) else json.dumps(content)
