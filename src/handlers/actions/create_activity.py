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
        stored_strava_credentials = self.database.get_strava_credentials(self.owner_id)
        # refresh credentials
        strava_client = StravaClient(
            stored_strava_credentials["access_token"],
            stored_strava_credentials["refresh_token"],
            int(stored_strava_credentials["expires_at"]),
        )
        refresh_strava_token(self.owner_id, strava_client, self.database)
        # fetch Strava activity data
        activity = strava_client.get_activity(self.object_id)
        activity = {k: activity[k] for k in STRAVA_ACTIVITY_FIELDS}
        # fetch Notion database id and Notion credentials of owner
        bot_id = self.database.get_notion_bot_id_from_athlete(self.owner_id)
        database_id = self.database.get_notion_database_id(bot_id)
        notion_access_token = self.database.get_notion_access_token(bot_id)
        # add a new page in Notion database with activity data
        notion_client = NotionClient(notion_access_token)
        properties = strava_activity_to_notion_properties(activity)
        page = notion_client.create_page(database_id, properties)

        return {"code": 200, "message": f"page {page['id']} created"}
