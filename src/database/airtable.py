"""Concrete implementation of database with airtable."""
import os

from src.airtable.client import Client
from src.airtable.types import Record
from src.database.interface import DatabaseInterface
from src.types.database import StravaToken
from src.utils.exceptions import InternalException, MissingEnvironmentVariable


class AirtableDatabase(DatabaseInterface):
    """
    Concrete implementation of DatabaseInterface.

    This implementation uses airtable.
    """

    def __init__(self):
        """Init instance."""
        self.pat = os.getenv("AIRTABLE_PAT")
        self.base_id = os.getenv("AIRTABLE_BASE_ID")
        self.strava_table_id = os.getenv("AIRTABLE_TABLE_STRAVA_ID")
        self.rel_strava_notion_table_id = os.getenv(
            "AIRTABLE_TABLE_REL_STRAVA_NOTION_ID"
        )
        self.notion_table_id = os.getenv("AIRTABLE_TABLE_NOTION")

        for var, name in [
            (self.pat, "AIRTABLE_PAT"),
            (self.base_id, "AIRTABLE_BASE_ID"),
            (self.strava_table_id, "AIRTABLE_TABLE_STRAVA_ID"),
            (self.rel_strava_notion_table_id, "AIRTABLE_TABLE_REL_STRAVA_NOTION_ID"),
            (self.notion_table_id, "AIRTABLE_TABLE_NOTION"),
        ]:
            if var is None:
                raise MissingEnvironmentVariable(name)

        self.client = Client(self.pat)

    def _get_single_record_by_id(self, key: str, value: str, table_id: str) -> Record:
        """
        Return a record of athlete if exists.

        :param key: name of the column
        :param value:
        :param table_id:
        :return:
        """
        _filter = f"{key}='{value}'"
        records = self.client.list_records(
            self.base_id, table_id, {"filterByFormula": _filter}
        )["records"]
        if len(records) == 0:
            raise InternalException(
                f"no record found in table {table_id} for {key} : {value}"
            )
        elif len(records) == 1:
            return records[0]
        else:
            raise InternalException(f"{len(records)} records found for {key} : {value}")

    def get_strava_credentials(self, athlete_id: str) -> StravaToken:
        """
        Fetch Strava tokens from airtable.

        :param athlete_id:
        :return:
        """
        record = self._get_single_record_by_id(
            "athlete_id", athlete_id, self.strava_table_id
        )
        fields = record["fields"]
        return {
            "access_token": fields["access_token"],
            "refresh_token": fields["refresh_token"],
            "expires_at": fields["expires_at"],
        }

    def update_strava_credentials(self, athlete_id: str, token: StravaToken) -> None:
        """
        Update the strava credentials with refresh token.

        :param athlete_id:
        :param token:
        :return:
        """
        record_id = self._get_single_record_by_id(
            "athlete_id", athlete_id, self.strava_table_id
        )["id"]
        body = {
            "fields": {
                "access_token": token["access_token"],
                "refresh_token": token["refresh_token"],
                "expires_at": token["expires_at"],
            },
            "returnFieldsByFieldId": None,
            "typecast": None,
        }
        self.client.update_record(self.base_id, self.strava_table_id, record_id, body)

    def get_notion_bot_id_from_athlete(self, athlete_id: str) -> str:
        """
        Return the Notion bot id.

        It uses the relation table rel_strava_notion

        :param athlete_id:
        :return:
        """
        record = self._get_single_record_by_id(
            "athlete_id", athlete_id, self.rel_strava_notion_table_id
        )
        return record["fields"]["notion_bot_id"]

    def get_notion_database_id(self, bot_id: str) -> str:
        """
        Return the Notion database id from the bot id.

        :param bot_id:
        :return:
        """
        record = self._get_single_record_by_id("bot_id", bot_id, self.notion_table_id)
        return record["fields"]["database_id"]

    def get_notion_access_token(self, bot_id: str) -> str:
        """
        Return the Notion access token.

        :param bot_id:
        :return:
        """
        record = self._get_single_record_by_id("bot_id", bot_id, self.notion_table_id)
        return record["fields"]["access_token"]
