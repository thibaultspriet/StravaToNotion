"""Implement the concrete action : CreateActivity."""
from src.const import STRAVA_ACTIVITY_FIELDS
from src.database.interface import DatabaseInterface
from src.handlers.actions import Action
from src.notion.client import Client as NotionClient
from src.strava.client import Client as StravaClient
from src.types.action import RunReturn
from src.workflows import refresh_strava_token, strava_activity_to_notion_properties


class CreateActivity(Action):
    """Concrete Action that add a page in the Strava database when a new activity is uploaded."""

    def __init__(
        self, owner_id: str, object_id: str, database_client: DatabaseInterface
    ):
        """
        Init instance.

        :param owner_id:
        :param object_id:
        :param database_client:
        """
        super().__init__(owner_id, object_id, database_client)

    def run(self) -> RunReturn:
        """Execute actions to create an activity."""
        # get Strava credentials of owner
        accounts = self.database.get_athlete_accounts(self.owner_id)
        message = []
        for account in accounts:
            stored_strava_credentials = self.database.get_strava_credentials(
                self.owner_id, account
            )
            # refresh credentials
            strava_client = StravaClient(
                stored_strava_credentials["access_token"],
                stored_strava_credentials["refresh_token"],
                int(stored_strava_credentials["expires_at"]),
            )
            refresh_strava_token(self.owner_id, account, strava_client, self.database)
            # fetch Strava activity data
            athlete_username = self.database.get_athlete_username(
                self.owner_id, account
            )
            activity = strava_client.get_activity(self.object_id)
            activity = {k: activity[k] for k in STRAVA_ACTIVITY_FIELDS}
            properties = strava_activity_to_notion_properties(
                {**activity, "username": athlete_username}
            )

            databases = self.database.list_databases(self.owner_id, account)
            for database in databases:
                try:
                    notion_access_token = self.database.get_notion_access_token(
                        database["bot_id"]
                    )
                    # add a new page in Notion database with activity data
                    notion_client = NotionClient(notion_access_token)
                    page = notion_client.create_page(
                        database["database_id"], properties
                    )
                    message.append(
                        f"page {page['id']} created for bot_id {database['bot_id']}, account {account}"
                    )
                except Exception as e:
                    message.append(
                        f"add activity {self.object_id} to bot_id {database['bot_id']} account {account} failed because: {e}"
                    )
        return {"code": 200, "message": "\n".join(message)}
