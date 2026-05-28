# chartspeak

Generate charts from a polars DataFrame and a natural-language prompt.

```python
import chartspeak as cs

fig = cs.generate_visualization(df, "histogram of costs")
```

## Installation

Core (matplotlib backend, offline via Ollama):

```bash
pip install chartspeak
```

With Ollama support (default local backend):

```bash
pip install "chartspeak[ollama]"
```

With all optional backends and renderers:

```bash
pip install "chartspeak[all]"
```

### Running Ollama locally

chartspeak uses [Ollama](https://ollama.com) by default. Install it and pull a model:

```bash
ollama pull qwen2.5:3b
```

## Quick start

```python
import polars as pl
import chartspeak as cs

df = pl.read_csv("data.csv")

# returns a matplotlib Figure
fig = cs.generate_visualization(df, "bar chart of sales by region")

# use a specific backend or engine
fig = cs.generate_visualization(df, "scatter of price vs quantity", engine="matplotlib")

# get the full result with spec, figure, and refine support
result = cs.generate_visualization(df, "line chart of revenue over time", return_result=True)
print(result.to_json())   # inspect the ChartSpec
```

## Optional dependencies

| Extra | Installs | Use case |
|---|---|---|
| `ollama` | `ollama` | Local LLM via Ollama (default backend) |
| `llamacpp` | `llama-cpp-python` | Local GGUF models |
| `api` | `litellm` | OpenAI-compatible APIs (OpenRouter, Groq, vLLM, ...) |
| `plotly` | `plotly` | Interactive charts |
| `all` | all of the above | Everything |
| `dev` | `pytest`, `ruff`, `mypy` | Development |

## Requirements

- Python 3.10+
- polars
- pydantic >= 2
- matplotlib
