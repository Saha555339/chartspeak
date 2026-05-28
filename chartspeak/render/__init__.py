import chartspeak.render.matplotlib  # noqa: F401  register matplotlib renderers on import
from chartspeak.render.base import get_renderer, register

__all__ = ["get_renderer", "register"]
