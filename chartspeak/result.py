from __future__ import annotations

import json
from typing import Any

import polars as pl

from chartspeak.spec import ChartSpec


class VizResult:
    """Container for a generated visualisation and its metadata."""

    def __init__(
        self,
        spec: ChartSpec,
        figure: Any,
        raw: str,
        prompt: str,
        backend: Any,
        engine: str,
        df: pl.DataFrame | None = None,
    ) -> None:
        self.spec = spec
        self.figure = figure
        self.raw = raw
        self.prompt = prompt
        self._backend = backend
        self._engine = engine
        self._df = df

    def refine(self, prompt: str) -> VizResult:
        """Produce a new VizResult by refining the current spec with a new prompt."""
        if self._df is None:
            raise RuntimeError(
                "DataFrame not stored; pass return_result=True from generate_visualization."
            )
        from chartspeak.api import generate_visualization

        result: VizResult = generate_visualization(
            self._df,
            prompt,
            backend=self._backend,
            engine=self._engine,
            return_result=True,
        )
        return result

    def to_json(self) -> str:
        """Serialise the spec to JSON."""
        return self.spec.model_dump_json(indent=2)

    def _repr_html_(self) -> str:
        import base64
        import io

        try:
            buf = io.BytesIO()
            self.figure.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode()
            img_tag = f'<img src="data:image/png;base64,{img_b64}" />'
        except Exception:
            img_tag = "<p>(figure not renderable)</p>"

        spec_json = json.dumps(json.loads(self.to_json()), indent=2)
        return (
            f"<div>{img_tag}"
            f"<details><summary>ChartSpec</summary>"
            f"<pre>{spec_json}</pre></details></div>"
        )
