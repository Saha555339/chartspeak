import polars as pl
import pytest

from chartspeak.schema import describe


def test_row_count(sample_df):
    schema = describe(sample_df)
    assert schema.n_rows == 7


def test_column_names(sample_df):
    schema = describe(sample_df)
    names = [c.name for c in schema.columns]
    assert names == ["category", "value", "count", "label"]


def test_dtype_strings(sample_df):
    schema = describe(sample_df)
    col = next(c for c in schema.columns if c.name == "value")
    assert "Float" in col.dtype or "float" in col.dtype.lower()


def test_nunique(sample_df):
    schema = describe(sample_df)
    col = next(c for c in schema.columns if c.name == "category")
    assert col.nunique == 3


def test_null_fraction_zero(sample_df):
    schema = describe(sample_df)
    for col in schema.columns:
        assert col.null_fraction == 0.0


def test_null_fraction_nonzero():
    df = pl.DataFrame({"a": [1, None, None, 4]})
    schema = describe(df)
    assert schema.columns[0].null_fraction == pytest.approx(0.5)


def test_samples_count(sample_df):
    schema = describe(sample_df, n_samples=2)
    for col in schema.columns:
        assert len(col.samples) <= 2


def test_to_prompt_contains_column(sample_df):
    schema = describe(sample_df)
    prompt = schema.to_prompt()
    assert "category" in prompt
    assert "value" in prompt
    assert "7 rows" in prompt
