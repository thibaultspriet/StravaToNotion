"""Implement an abstract class Action."""
from abc import abstractmethod

from src.database.interface import DatabaseInterface
from src.types.action import RunReturn


class Action:
    """Abstract class to handle response to Strava events."""

    def __init__(
        self, owner_id: str, object_id: str, database_client: DatabaseInterface
    ):
        """
        Init instance.

        :param owner_id: Strava user's id
        :param object_id: id of Strava object relative to the event (either an activity id or an athlete id)
        """
        self.owner_id = owner_id
        self.object_id = object_id
        self.database = database_client

    @abstractmethod
    def run(self) -> RunReturn:
        """
        Execute the action.

        Implemented by concrete classes
        """
        pass
