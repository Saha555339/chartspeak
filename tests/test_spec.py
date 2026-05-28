import pytest
from pydantic import ValidationError

from chartspeak.spec import ChartSpec


def test_minimal_spec():
    spec = ChartSpec(chart="histogram", x="value")
    assert spec.version == 1
    assert spec.bins == 30
    assert spec.log_x is False


def test_full_spec():
    spec = ChartSpec(
        chart="bar",
        x="category",
        y="value",
        agg="mean",
        title="Test",
        log_y=True,
    )
    assert spec.agg == "mean"
    assert spec.title == "Test"


def test_invalid_chart_type():
    with pytest.raises(ValidationError):
        ChartSpec(chart="unknown", x="col")


def test_json_schema_has_required():
    schema = ChartSpec.json_schema()
    assert "properties" in schema
    assert "chart" in schema["properties"]
    assert "x" in schema["properties"]


def test_roundtrip_json():
    spec = ChartSpec(chart="scatter", x="a", y="b")
    recovered = ChartSpec.model_validate_json(spec.model_dump_json())
    assert recovered == spec
