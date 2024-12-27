"""Implement the concrete action : UpdateActivity."""
from src.const import STRAVA_ACTIVITY_FIELDS
from src.handlers.actions import Action
from src.notion.client import Client as NotionClient
from src.notion.utils import get_ids_of_page_activity
from src.strava.client import Client as StravaClient
from src.types.action import RunReturn
from src.workflows import refresh_strava_token, strava_activity_to_notion_properties


class UpdateActivity(Action):
    """Concrete Action that update a page in the Strava database when an activity is uploaded."""

    def run(self) -> RunReturn:
        """Execute actions to updata an activity."""
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
        athlete_username = self.database.get_athlete_username(self.owner_id)
        # fetch Notion database id and Notion credentials of owner
        databases = self.database.list_databases(self.owner_id)
        message = []
        for database in databases:
            bot_id = database["bot_id"]
            database_id = database["database_id"]
            try:
                notion_access_token = self.database.get_notion_access_token(bot_id)
                # get pages from database relative to the activity
                notion_client = NotionClient(notion_access_token)
                page_ids = get_ids_of_page_activity(
                    notion_client, database_id, self.object_id
                )
                # update the properties of the pages
                updated_pages = []
                if len(page_ids) >= 1:
                    for id_ in page_ids:
                        properties = strava_activity_to_notion_properties(
                            {**activity, "username": athlete_username}
                        )
                        notion_client.update_page_properties(id_, properties)
                        updated_pages.append(id_)
                else:
                    properties = strava_activity_to_notion_properties(
                        {**activity, "username": athlete_username}
                    )
                    page = notion_client.create_page(database_id, properties)
                    updated_pages.append(page["id"])
                message.append(
                    f"page {', '.join(updated_pages)} updated on database {database_id}"
                )
            except Exception as e:
                message.append(
                    f"failed to update page on database {database_id} because {e}"
                )

        return {"code": 200, "message": "\n".join(message)}
