import polars as pl
import pytest

from chartspeak.api import generate_spec
from chartspeak.backends.mock import MockBackend
from chartspeak.errors import RepairFailedError


@pytest.fixture
def df():
    return pl.DataFrame({"value": [1.0, 2.0, 3.0], "cat": ["A", "B", "C"]})


def test_repair_loop_fixes_invalid_spec(df):
    backend = MockBackend(
        [
            {"version": 1, "chart": "histogram", "x": "missing_col"},
            {"version": 1, "chart": "histogram", "x": "value"},
        ]
    )
    spec = generate_spec(df, "histogram of value", backend=backend, max_repair=2)
    assert spec.x == "value"
    assert backend._call_count == 2


def test_repair_loop_exhausted_raises(df):
    backend = MockBackend(
        [
            {"version": 1, "chart": "histogram", "x": "missing"},
            {"version": 1, "chart": "histogram", "x": "missing"},
            {"version": 1, "chart": "histogram", "x": "missing"},
        ]
    )
    with pytest.raises(RepairFailedError):
        generate_spec(df, "histogram", backend=backend, max_repair=2)
    assert backend._call_count == 3


def test_repair_loop_no_repair_needed(df):
    backend = MockBackend([{"version": 1, "chart": "histogram", "x": "value"}])
    spec = generate_spec(df, "histogram", backend=backend, max_repair=2)
    assert spec.x == "value"
    assert backend._call_count == 1
