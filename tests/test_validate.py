import polars as pl
import pytest

from chartspeak.errors import SpecValidationError
from chartspeak.spec import ChartSpec
from chartspeak.validate import validate_spec


@pytest.fixture
def df():
    return pl.DataFrame(
        {
            "cat": ["A", "B", "C"],
            "num": [1.0, 2.0, 3.0],
        }
    )


def test_valid_histogram(df):
    spec = ChartSpec(chart="histogram", x="num")
    validate_spec(spec, df)


def test_histogram_non_numeric_x_raises(df):
    spec = ChartSpec(chart="histogram", x="cat")
    with pytest.raises(SpecValidationError, match="numeric"):
        validate_spec(spec, df)


def test_missing_x_raises(df):
    spec = ChartSpec(chart="histogram", x="missing")
    with pytest.raises(SpecValidationError, match="missing"):
        validate_spec(spec, df)


def test_missing_y_raises(df):
    spec = ChartSpec(chart="bar", x="cat", y="missing", agg="sum")
    with pytest.raises(SpecValidationError, match="missing"):
        validate_spec(spec, df)


def test_missing_group_by_raises(df):
    spec = ChartSpec(chart="bar", x="cat", y="num", group_by="missing", agg="sum")
    with pytest.raises(SpecValidationError, match="missing"):
        validate_spec(spec, df)


def test_bar_categorical_without_agg_raises(df):
    spec = ChartSpec(chart="bar", x="cat", y="num")
    with pytest.raises(SpecValidationError, match="agg"):
        validate_spec(spec, df)


def test_bar_categorical_with_agg_ok(df):
    spec = ChartSpec(chart="bar", x="cat", y="num", agg="mean")
    validate_spec(spec, df)


def test_scatter_non_numeric_y_raises(df):
    spec = ChartSpec(chart="scatter", x="num", y="cat")
    with pytest.raises(SpecValidationError, match="numeric"):
        validate_spec(spec, df)


def test_line_group_by_without_agg_raises(df):
    spec = ChartSpec(chart="line", x="num", y="num", group_by="cat")
    with pytest.raises(SpecValidationError, match="agg"):
        validate_spec(spec, df)
