from typing import Any

import polars as pl
from pydantic import BaseModel


class ColumnInfo(BaseModel):
    name: str
    dtype: str
    nunique: int
    null_fraction: float
    samples: list[Any]


class DatasetSchema(BaseModel):
    n_rows: int
    columns: list[ColumnInfo]

    def to_prompt(self) -> str:
        """Return compact text representation for LLM context."""
        lines = [f"Dataset: {self.n_rows} rows, {len(self.columns)} columns"]
        for col in self.columns:
            sample_str = ", ".join(repr(s) for s in col.samples)
            lines.append(
                f"  {col.name} ({col.dtype}): {col.nunique} unique"
                f", {col.null_fraction:.1%} null, samples=[{sample_str}]"
            )
        return "\n".join(lines)


def describe(df: pl.DataFrame, n_samples: int = 3) -> DatasetSchema:
    """Produce a compact schema description of df."""
    columns: list[ColumnInfo] = []
    for col_name in df.columns:
        series = df[col_name]
        nunique = series.n_unique()
        null_fraction = series.null_count() / len(series) if len(series) > 0 else 0.0
        non_null = series.drop_nulls()
        samples: list[Any] = non_null.head(n_samples).to_list()
        columns.append(
            ColumnInfo(
                name=col_name,
                dtype=str(series.dtype),
                nunique=nunique,
                null_fraction=null_fraction,
                samples=samples,
            )
        )
    return DatasetSchema(n_rows=len(df), columns=columns)
