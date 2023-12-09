"""Types relative to Strava."""
from typing import TypedDict


class Token(TypedDict):
    """Type of Strava token."""

    access_token: str
    expires_at: int
    refresh_token: str
