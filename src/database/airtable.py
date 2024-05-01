"""Concrete implementation of database with airtable."""
import json
import os
from typing import Union

from src.airtable.client import Client
from src.airtable.types import Record
from src.database.interface import DatabaseInterface
from src.types.database import StravaToken
from src.types.oauth import NotionCredentials, OauthCredentials, StravaCredentials
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

    def _get_single_record_by_id(
        self, key: Union[str, list[str]], value: Union[str, list[str]], table_id: str
    ) -> Record:
        """
        Return a record of athlete if exists.

        :param key: name of the column
        :param value:
        :param table_id:
        :return:
        """
        if isinstance(key, str):
            key = [key]
            value = [value]
        _filter = ", ".join([f"{k}='{v}'" for k, v in zip(key, value)])
        _filter = f"AND({_filter})"
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

    def _record_exist(
        self, key: Union[str, list[str]], value: Union[str, list[str]], table_id: str
    ) -> bool:
        """
        Check if a record identified with a key, value exists in the table.

        :param key:
        :param value:
        :param table_id:
        :return:
        """
        if isinstance(key, str):
            key = [key]
            value = [value]
        _filter = ", ".join([f"{k}='{v}'" for k, v in zip(key, value)])
        _filter = f"AND({_filter})"
        records = self.client.list_records(
            self.base_id, table_id, {"filterByFormula": _filter}
        )["records"]
        return len(records) > 0

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
        record = self._get_single_record_by_id(
            ["user_email", "athlete_id", "notion_bot_id"],
            [user_email, athlete_id, bot_id],
            self.rel_strava_notion_table_id,
        )
        return record["fields"].get("database_id")

    def get_notion_access_token(self, bot_id: str) -> str:
        """
        Return the Notion access token.

        :param bot_id:
        :return:
        """
        record = self._get_single_record_by_id("bot_id", bot_id, self.notion_table_id)
        return record["fields"]["access_token"]

    def add_or_update_user(self, credentials: OauthCredentials) -> None:
        """
        Add or update a user.

        It add or update the tables : oauth (for Strava), rel_strava_notion and notion.
        :param credentials:
        :return:
        """
        self._add_or_update_strava(credentials["strava"])
        self._add_or_update_rel(
            credentials["strava"]["athlete"],
            credentials["notion"]["bot_id"],
            credentials["user_email"],
        )
        self._add_or_update_notion(credentials["notion"])

    def update_database_id(
        self, user_email: str, athlete_id: str, bot_id: str, database_id: str
    ) -> None:
        """
        Update the database id in the notion table.

        :param user_email:
        :param athlete_id:
        :param bot_id:
        :param database_id:
        :return:
        """
        record_id = self._get_single_record_by_id(
            ["user_email", "athlete_id", "notion_bot_id"],
            [user_email, athlete_id, bot_id],
            self.rel_strava_notion_table_id,
        )["id"]

        body = {
            "fields": {"database_id": database_id},
            "returnFieldsByFieldId": None,
            "typecast": None,
        }
        self.client.update_record(self.base_id, self.notion_table_id, record_id, body)

    def _add_or_update_strava(self, strava_credentials: StravaCredentials) -> None:
        """
        Add or update the Strava table.

        :param strava_credentials:
        :return:
        """
        athlete_id = strava_credentials["athlete"]
        if self._record_exist("athlete_id", athlete_id, self.strava_table_id):
            self.update_strava_credentials(athlete_id, strava_credentials)
        else:
            _fields = {
                "athlete_id": athlete_id,
                "token_type": "Bearer",
                "expires_at": strava_credentials["expires_at"],
                "refresh_token": strava_credentials["refresh_token"],
                "expires_in": "21600",
                "access_token": strava_credentials["access_token"],
            }
            body = {
                "fields": _fields,
                "returnFieldsByFieldId": None,
                "typecast": None,
                "records": None,
            }
            self.client.create_records(self.base_id, self.strava_table_id, body)

    def _add_or_update_rel(self, athlete: str, bot_id: str, user_email: str) -> None:
        """
        Add or update relation table.

        :param athlete:
        :param bot_id:
        :param user_email:
        :return:
        """
        fields = {
            "athlete_id": athlete,
            "notion_bot_id": bot_id,
            "user_email": user_email,
        }
        if self._record_exist(
            ["user_email", "athlete_id", "notion_bot_id"],
            [user_email, athlete, bot_id],
            self.rel_strava_notion_table_id,
        ):
            record_id = self._get_single_record_by_id(
                ["user_email", "athlete_id", "notion_bot_id"],
                [user_email, athlete, bot_id],
                self.rel_strava_notion_table_id,
            )["id"]
            body = {
                "fields": fields,
                "returnFieldsByFieldId": None,
                "typecast": None,
            }
            self.client.update_record(
                self.base_id, self.rel_strava_notion_table_id, record_id, body
            )
        else:
            body = {
                "fields": fields,
                "returnFieldsByFieldId": None,
                "typecast": None,
                "records": None,
            }
            self.client.create_records(
                self.base_id, self.rel_strava_notion_table_id, body
            )

    def _add_or_update_notion(self, credentials: NotionCredentials) -> None:
        """
        Add or update user's Notion credentials.

        :param credentials:
        :return:
        """
        fields = {
            "bot_id": credentials["bot_id"],
            "access_token": credentials["access_token"],
            "duplicated_template_id": credentials["duplicated_template_id"],
            "owner": json.dumps(credentials["owner"]),
            "workspace_icon": credentials["workspace_icon"],
            "workspace_id": credentials["workspace_id"],
            "workspace_name": credentials["workspace_name"],
        }
        if self._record_exist("bot_id", fields["bot_id"], self.notion_table_id):
            record_id = self._get_single_record_by_id(
                "bot_id", fields["bot_id"], self.notion_table_id
            )["id"]
            body = {
                "fields": fields,
                "returnFieldsByFieldId": None,
                "typecast": None,
            }
            self.client.update_record(
                self.base_id, self.notion_table_id, record_id, body
            )
        else:
            body = {
                "fields": fields,
                "returnFieldsByFieldId": None,
                "typecast": None,
                "records": None,
            }
            self.client.create_records(self.base_id, self.notion_table_id, body)
