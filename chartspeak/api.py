from __future__ import annotations

import logging
from typing import Any

import polars as pl

from chartspeak.backends.base import Backend
from chartspeak.backends.ollama import OllamaBackend
from chartspeak.errors import RepairFailedError
from chartspeak.prompts import SYSTEM_PROMPT, build_repair_prompt, build_user_prompt
from chartspeak.render import get_renderer
from chartspeak.schema import describe
from chartspeak.spec import ChartSpec
from chartspeak.validate import validate_spec

logger = logging.getLogger(__name__)


def _resolve_backend(backend: Backend | str | None) -> Backend:
    if backend is None:
        return OllamaBackend()
    if isinstance(backend, str):
        from chartspeak.backends import get_backend

        return get_backend(backend)
    return backend


def _to_polars(df: Any) -> pl.DataFrame:
    if isinstance(df, pl.DataFrame):
        return df
    try:
        return pl.from_pandas(df)
    except Exception as e:
        raise TypeError(f"Unsupported DataFrame type: {type(df)}") from e


def generate_spec(
    df: Any,
    prompt: str,
    *,
    backend: Backend | str | None = None,
    max_repair: int = 2,
) -> ChartSpec:
    """Generate a ChartSpec from a DataFrame and a natural-language prompt."""
    frame = _to_polars(df)
    bk = _resolve_backend(backend)
    schema = describe(frame)
    dataset_desc = schema.to_prompt()
    json_schema = ChartSpec.json_schema()

    user_msg = build_user_prompt(dataset_desc, prompt)
    raw = bk.spec(SYSTEM_PROMPT, user_msg, json_schema)

    last_error: Exception = RuntimeError("No attempts made.")
    for attempt in range(max_repair + 1):
        try:
            spec = ChartSpec.model_validate_json(raw)
            validate_spec(spec, frame)
            return spec
        except Exception as e:
            last_error = e
            logger.debug("Attempt %d failed: %s", attempt + 1, e)
            if attempt < max_repair:
                repair_msg = build_repair_prompt(dataset_desc, prompt, raw, str(e))
                raw = bk.spec(SYSTEM_PROMPT, repair_msg, json_schema)

    raise RepairFailedError(
        f"Failed to produce a valid spec after {max_repair + 1} attempts."
    ) from last_error


def generate_visualization(
    df: Any,
    prompt: str,
    *,
    backend: Backend | str | None = None,
    engine: str = "matplotlib",
    max_repair: int = 2,
    return_result: bool = False,
) -> Any:
    """Generate a visualization from a DataFrame and a natural-language prompt.

    Returns the figure object by default, or a VizResult when return_result=True.
    """
    frame = _to_polars(df)
    spec = generate_spec(frame, prompt, backend=backend, max_repair=max_repair)
    renderer = get_renderer(engine, spec.chart)
    figure = renderer(spec, frame)

    if not return_result:
        return figure

    from chartspeak.result import VizResult

    bk = _resolve_backend(backend)
    return VizResult(spec=spec, figure=figure, raw="", prompt=prompt, backend=bk, engine=engine)
