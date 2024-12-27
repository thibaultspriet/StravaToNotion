"""Declare the database interface."""
from abc import ABC, abstractmethod

from src.types.database import StravaToken
from src.types.oauth import OauthCredentials, StravaAthleteInfo


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
    def get_notion_database_id(
        self, user_email: str, athlete_id: str, bot_id: str
    ) -> str:
        """
        Return the Notion database id from the bot id.

        :param user_email:
        :param athlete_id:
        :param bot_id:
        :return:
        """
        pass

    @abstractmethod
    def list_databases(self, athlete_id: str) -> list[dict]:
        """
        Return a list of Notion databases registered for a Strava athlete id.

        :param athlete_id:
        :return: list of dict with keys : bot_id & database_id
        """

    @abstractmethod
    def get_notion_access_token(self, bot_id: str) -> str:
        """
        Return the Notion access token.

        :param bot_id:
        :return:
        """

    @abstractmethod
    def add_or_update_user(
        self, credentials: OauthCredentials, athlete_info: StravaAthleteInfo
    ) -> None:
        """
        Add or update a user.

        A user is identified with both its credentials for Strava and Notion.
        :param credentials:
        :param athlete_info:
        :return:
        """

    @abstractmethod
    def update_database_id(
        self, user_email: str, athlete_id: str, bot_id: str, database_id: str
    ) -> None:
        """
        Update the Strava activities database id.

        :param user_email:
        :param athlete_id:
        :param bot_id:
        :param database_id:
        :return:
        """

    @abstractmethod
    def get_athlete_username(self, athlete_id: str) -> str:
        """
        Return the username of the identified athlete.

        :param athlete_id:
        :return:
        """
        pass
