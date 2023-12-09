"""Types relative to Action class."""
from typing import TypedDict


class RunReturn(TypedDict):
    """Returned type of method run."""

    code: int
    message: str
