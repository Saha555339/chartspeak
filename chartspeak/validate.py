import polars as pl

from chartspeak.errors import SpecValidationError
from chartspeak.spec import ChartSpec

_NUMERIC_DTYPES = {
    pl.Int8,
    pl.Int16,
    pl.Int32,
    pl.Int64,
    pl.UInt8,
    pl.UInt16,
    pl.UInt32,
    pl.UInt64,
    pl.Float32,
    pl.Float64,
}

_CHARTS_REQUIRING_NUMERIC_Y = {"line", "scatter", "box"}
_CHARTS_REQUIRING_AGG = {"bar", "line"}


def _is_numeric(series: pl.Series) -> bool:
    return type(series.dtype) in _NUMERIC_DTYPES or series.dtype in _NUMERIC_DTYPES


def validate_spec(spec: ChartSpec, df: pl.DataFrame) -> None:
    """Validate spec semantics against df; raise SpecValidationError on failure."""
    col_names = set(df.columns)

    if spec.x not in col_names:
        raise SpecValidationError(f"Column '{spec.x}' not found in dataset.")

    if spec.y is not None and spec.y not in col_names:
        raise SpecValidationError(f"Column '{spec.y}' not found in dataset.")

    if spec.group_by is not None and spec.group_by not in col_names:
        raise SpecValidationError(f"Column '{spec.group_by}' not found in dataset.")

    if spec.chart == "histogram" and not _is_numeric(df[spec.x]):
        raise SpecValidationError(
            f"histogram requires numeric x column, but '{spec.x}' is {df[spec.x].dtype}."
        )

    if spec.chart in _CHARTS_REQUIRING_NUMERIC_Y and spec.y is not None:
        if not _is_numeric(df[spec.y]):
            raise SpecValidationError(
                f"'{spec.chart}' requires numeric y column, but '{spec.y}' is {df[spec.y].dtype}."
            )

    needs_agg = spec.chart in _CHARTS_REQUIRING_AGG and (
        spec.group_by is not None or not _is_numeric(df[spec.x])
    )
    if needs_agg and spec.agg is None:
        raise SpecValidationError(
            f"'{spec.chart}' with categorical x or group_by requires 'agg' to be set."
        )
