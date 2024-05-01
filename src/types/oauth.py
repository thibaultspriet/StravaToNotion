"""Custom types for Oauth."""
from typing import TypedDict


class StravaCredentials(TypedDict):
    """Type of Strava credentials."""

    access_token: str
    refresh_token: str
    expires_at: str
    athlete: str


class NotionCredentials(TypedDict):
    """Type of Notion credentials."""

    access_token: str
    bot_id: str
    duplicated_template_id: str
    owner: dict
    workspace_icon: str
    workspace_id: str
    workspace_name: str


class OauthCredentials(TypedDict):
    """Type of Oauth credentials."""

    strava: StravaCredentials
    notion: NotionCredentials
    user_email: str
