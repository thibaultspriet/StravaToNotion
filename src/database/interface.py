"""Declare the database interface."""
from abc import ABC, abstractmethod

from src.types.database import StravaToken
from src.types.oauth import OauthCredentials


class DatabaseInterface(ABC):
    """Database interface."""

    @abstractmethod
    def get_strava_credentials(self, athlete_id: str) -> StravaToken:
        """
        Retrieve Strava tokens for a given athlete.

        :param athlete_id:
        :return:
        """
        pass

    @abstractmethod
    def update_strava_credentials(self, athlete_id: str, token: StravaToken) -> None:
        """
        Update existing Strava credentials of a user in the database.

        :param athlete_id:
        :param token:
        :return:
        """
        pass

    @abstractmethod
    def get_notion_bot_id_from_athlete(self, athlete_id: str) -> str:
        """
        Return the Notion bot id based on the Strava athlete id.

        :param athlete_id:
        :return:
        """
        pass

    @abstractmethod
    def get_notion_database_id(self, bot_id: str) -> str:
        """
        Return the Notion database id from the bot id.

        :param bot_id:
        :return:
        """
        pass

    @abstractmethod
    def get_notion_access_token(self, bot_id: str) -> str:
        """
        Return the Notion access token.

        :param bot_id:
        :return:
        """

    @abstractmethod
    def add_or_update_user(self, credentials: OauthCredentials) -> None:
        """
        Add or update a user.

        A user is identified with both its credentials for Strava and Notion.
        :param credentials:
        :return:
        """

    @abstractmethod
    def update_database_id(self, bot_id: str, database_id: str) -> None:
        """
        Update the Strava activities database id.

        :param bot_id:
        :param database_id:
        :return:
        """
