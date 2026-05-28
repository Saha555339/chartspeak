import json
from collections.abc import Callable
from typing import Any

from chartspeak.backends.base import Backend


class MockBackend(Backend):
    """Backend for testing; returns preset responses without any LLM call."""

    def __init__(self, responses: list[dict[str, Any]] | Callable[[str], dict[str, Any]]) -> None:
        if isinstance(responses, list):
            self._responses = iter(responses)
            self._fn: Callable[[str], dict[str, Any]] | None = None
        else:
            self._responses = iter([])
            self._fn = responses
        self._call_count = 0

    def spec(self, system: str, user: str, json_schema: dict[str, Any]) -> str:
        self._call_count += 1
        if self._fn is not None:
            return json.dumps(self._fn(user))
        return json.dumps(next(self._responses))
