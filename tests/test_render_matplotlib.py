import matplotlib.pyplot as plt
import polars as pl
import pytest

from chartspeak.render import get_renderer
from chartspeak.spec import ChartSpec


@pytest.fixture
def df():
    return pl.DataFrame(
        {
            "cat": ["A", "B", "C", "A", "B"],
            "num": [1.0, 2.0, 3.0, 4.0, 5.0],
            "num2": [5.0, 4.0, 3.0, 2.0, 1.0],
        }
    )


def _render(spec: ChartSpec, df: pl.DataFrame) -> plt.Figure:
    renderer = get_renderer("matplotlib", spec.chart)
    return renderer(spec, df)


def test_histogram_returns_figure(df):
    spec = ChartSpec(chart="histogram", x="num", title="My Hist")
    fig = _render(spec, df)
    assert isinstance(fig, plt.Figure)


def test_histogram_title(df):
    spec = ChartSpec(chart="histogram", x="num", title="Costs")
    fig = _render(spec, df)
    assert fig.axes[0].get_title() == "Costs"


def test_histogram_xlabel(df):
    spec = ChartSpec(chart="histogram", x="num")
    fig = _render(spec, df)
    assert fig.axes[0].get_xlabel() == "num"


def test_bar_returns_figure(df):
    spec = ChartSpec(chart="bar", x="cat", y="num", agg="mean")
    fig = _render(spec, df)
    assert isinstance(fig, plt.Figure)


def test_line_returns_figure(df):
    spec = ChartSpec(chart="line", x="num", y="num2")
    fig = _render(spec, df)
    assert isinstance(fig, plt.Figure)


def test_scatter_returns_figure(df):
    spec = ChartSpec(chart="scatter", x="num", y="num2")
    fig = _render(spec, df)
    assert isinstance(fig, plt.Figure)


def test_box_returns_figure(df):
    spec = ChartSpec(chart="box", x="num")
    fig = _render(spec, df)
    assert isinstance(fig, plt.Figure)


def test_box_with_group_by(df):
    spec = ChartSpec(chart="box", x="num", group_by="cat")
    fig = _render(spec, df)
    assert isinstance(fig, plt.Figure)


def test_unknown_renderer_raises():
    from chartspeak.errors import RendererNotFoundError

    with pytest.raises(RendererNotFoundError):
        get_renderer("matplotlib", "unknown_type")
