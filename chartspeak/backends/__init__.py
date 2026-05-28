from chartspeak.backends.base import Backend
from chartspeak.backends.mock import MockBackend
from chartspeak.backends.ollama import OllamaBackend

_REGISTRY: dict[str, type[Backend]] = {
    "ollama": OllamaBackend,
    "mock": MockBackend,
}


def get_backend(name: str, **kwargs: object) -> Backend:
    """Instantiate a registered backend by name."""
    if name not in _REGISTRY:
        available = ", ".join(_REGISTRY)
        raise ValueError(f"Unknown backend '{name}'. Available: {available}")
    return _REGISTRY[name](**kwargs)


__all__ = ["Backend", "MockBackend", "OllamaBackend", "get_backend"]
