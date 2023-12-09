"""Types for modules of database package."""
from typing import TypedDict


class StravaToken(TypedDict):
    """Strava token type."""

    refresh_token: str
    access_token: str
    expires_at: str
