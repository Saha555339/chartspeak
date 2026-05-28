from collections.abc import Callable
from typing import Any

import polars as pl

from chartspeak.errors import RendererNotFoundError
from chartspeak.spec import ChartSpec

_REGISTRY: dict[tuple[str, str], Callable[..., Any]] = {}


def register(engine: str, chart_type: str) -> Callable[..., Any]:
    """Decorator registering a render function for (engine, chart_type)."""

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        _REGISTRY[(engine, chart_type)] = fn
        return fn

    return decorator


def get_renderer(engine: str, chart_type: str) -> Callable[[ChartSpec, pl.DataFrame], Any]:
    """Return the renderer for (engine, chart_type) or raise RendererNotFoundError."""
    key = (engine, chart_type)
    if key not in _REGISTRY:
        raise RendererNotFoundError(
            f"No renderer for engine='{engine}', chart_type='{chart_type}'."
        )
    return _REGISTRY[key]
