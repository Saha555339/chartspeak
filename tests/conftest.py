import polars as pl
import pytest

from chartspeak.backends.mock import MockBackend


@pytest.fixture
def sample_df() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "category": ["A", "B", "C", "A", "B", "C", "A"],
            "value": [10.0, 20.0, 15.0, 30.0, 25.0, 5.0, 18.0],
            "count": [1, 2, 3, 4, 5, 6, 7],
            "label": ["x", "y", "z", "x", "y", "z", "x"],
        }
    )


@pytest.fixture
def mock_backend_histogram() -> MockBackend:
    return MockBackend(
        [{"version": 1, "chart": "histogram", "x": "value", "title": "Value distribution"}]
    )


@pytest.fixture
def mock_backend_bar() -> MockBackend:
    return MockBackend(
        [{"version": 1, "chart": "bar", "x": "category", "y": "value", "agg": "mean"}]
    )
