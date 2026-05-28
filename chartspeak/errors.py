class VizspecError(Exception):
    """Base exception for chartspeak."""


class SpecValidationError(VizspecError):
    """Raised when a ChartSpec fails semantic validation against a DataFrame."""


class BackendError(VizspecError):
    """Raised when a backend fails to produce a valid spec."""


class RendererNotFoundError(VizspecError):
    """Raised when no renderer is registered for a given engine/chart_type pair."""


class RepairFailedError(VizspecError):
    """Raised when the repair loop exhausts all attempts."""
