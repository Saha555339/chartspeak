import matplotlib.pyplot as plt
import polars as pl
import pytest

import chartspeak as vs
from chartspeak.backends.mock import MockBackend
from chartspeak.result import VizResult


@pytest.fixture
def df():
    return pl.DataFrame({"value": [1.0, 2.0, 3.0, 4.0, 5.0]})


def test_generate_visualization_returns_figure(df):
    backend = MockBackend([{"version": 1, "chart": "histogram", "x": "value"}])
    fig = vs.generate_visualization(df, "histogram of value", backend=backend)
    assert isinstance(fig, plt.Figure)


def test_generate_visualization_return_result(df):
    backend = MockBackend([{"version": 1, "chart": "histogram", "x": "value"}])
    result = vs.generate_visualization(df, "histogram", backend=backend, return_result=True)
    assert isinstance(result, VizResult)
    assert result.spec.chart == "histogram"


def test_generate_spec_returns_chart_spec(df):
    backend = MockBackend([{"version": 1, "chart": "histogram", "x": "value"}])
    spec = vs.generate_spec(df, "histogram", backend=backend)
    assert spec.chart == "histogram"
    assert spec.x == "value"


def test_mock_backend_call_count(df):
    backend = MockBackend([{"version": 1, "chart": "histogram", "x": "value"}])
    vs.generate_spec(df, "histogram", backend=backend)
    assert backend._call_count == 1


def test_pandas_adapter():
    pd = pytest.importorskip("pandas")
    pdf = pd.DataFrame({"value": [1.0, 2.0, 3.0]})
    backend = MockBackend([{"version": 1, "chart": "histogram", "x": "value"}])
    fig = vs.generate_visualization(pdf, "histogram", backend=backend)
    assert isinstance(fig, plt.Figure)
