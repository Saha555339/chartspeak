import matplotlib
import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot as plt
import polars as pl

from chartspeak.render.base import register
from chartspeak.spec import ChartSpec

matplotlib.use("Agg")

Figure = matplotlib.figure.Figure


def _apply_scale(ax: matplotlib.axes.Axes, spec: ChartSpec) -> None:
    if spec.log_x:
        ax.set_xscale("log")
    if spec.log_y:
        ax.set_yscale("log")


def _finalize(ax: matplotlib.axes.Axes, spec: ChartSpec) -> None:
    if spec.title:
        ax.set_title(spec.title)
    ax.set_xlabel(spec.x)
    if spec.y:
        ax.set_ylabel(spec.y)
    _apply_scale(ax, spec)


@register("matplotlib", "histogram")
def render_histogram(spec: ChartSpec, df: pl.DataFrame) -> Figure:
    fig, ax = plt.subplots()
    ax.hist(df[spec.x].drop_nulls().to_list(), bins=spec.bins)
    _finalize(ax, spec)
    return fig


@register("matplotlib", "bar")
def render_bar(spec: ChartSpec, df: pl.DataFrame) -> Figure:
    if spec.agg and spec.y:
        grouped = df.group_by(spec.x).agg(getattr(pl.col(spec.y), spec.agg)().alias(spec.y))
    else:
        grouped = df.select([spec.x, spec.y]) if spec.y else df.select([spec.x])

    x_vals = grouped[spec.x].to_list()
    y_col = spec.y or spec.x
    y_vals = grouped[y_col].to_list() if y_col in grouped.columns else [1] * len(x_vals)

    fig, ax = plt.subplots()
    ax.bar([str(v) for v in x_vals], y_vals)
    _finalize(ax, spec)
    return fig


@register("matplotlib", "line")
def render_line(spec: ChartSpec, df: pl.DataFrame) -> Figure:
    sorted_df = df.sort(spec.x) if spec.y else df

    if spec.agg and spec.y:
        sorted_df = (
            df.group_by(spec.x).agg(getattr(pl.col(spec.y), spec.agg)().alias(spec.y)).sort(spec.x)
        )

    x_vals = sorted_df[spec.x].to_list()
    y_vals = sorted_df[spec.y].to_list() if spec.y else list(range(len(x_vals)))

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    _finalize(ax, spec)
    return fig


@register("matplotlib", "scatter")
def render_scatter(spec: ChartSpec, df: pl.DataFrame) -> Figure:
    x_vals = df[spec.x].to_list()
    y_vals = df[spec.y].to_list() if spec.y else list(range(len(x_vals)))

    fig, ax = plt.subplots()
    ax.scatter(x_vals, y_vals)
    _finalize(ax, spec)
    return fig


@register("matplotlib", "box")
def render_box(spec: ChartSpec, df: pl.DataFrame) -> Figure:
    fig, ax = plt.subplots()

    if spec.group_by:
        groups = df[spec.group_by].unique().to_list()
        data = [
            df.filter(pl.col(spec.group_by) == g)[spec.x].drop_nulls().to_list() for g in groups
        ]
        ax.boxplot(data, tick_labels=[str(g) for g in groups])
    else:
        col = spec.y if spec.y else spec.x
        ax.boxplot(df[col].drop_nulls().to_list())

    if spec.title:
        ax.set_title(spec.title)
    ax.set_xlabel(spec.group_by or "")
    ax.set_ylabel(spec.y or spec.x)
    _apply_scale(ax, spec)
    return fig
