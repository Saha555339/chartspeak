from typing import Any, Literal

from pydantic import BaseModel

ChartType = Literal["histogram", "bar", "line", "scatter", "box", "pie"]
Agg = Literal["sum", "mean", "count", "median", "min", "max"]


class ChartSpec(BaseModel):
    """Validated, serialisable chart specification."""

    version: int = 1
    chart: ChartType
    x: str
    y: str | None = None
    group_by: str | None = None
    agg: Agg | None = None
    bins: int = 30
    log_x: bool = False
    log_y: bool = False
    title: str | None = None

    @classmethod
    def json_schema(cls) -> dict[str, Any]:
        """Return JSON Schema for constrained decoding backends."""
        return cls.model_json_schema()
