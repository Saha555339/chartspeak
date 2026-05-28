from abc import ABC, abstractmethod
from typing import Any


class Backend(ABC):
    """Abstract base for LLM backends that produce a JSON spec string."""

    @abstractmethod
    def spec(self, system: str, user: str, json_schema: dict[str, Any]) -> str:
        """Return a JSON string conforming to json_schema."""
