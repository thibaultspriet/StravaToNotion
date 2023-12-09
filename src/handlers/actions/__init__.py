"""
Package in which all actions (processing of Strava events) are defined.

An abstract class Action with a method run is defined. Exemple of actions :
- CreateActivity : when a new activity is uploaded on Strava, create a new page in Notion
- UpdateActivity : when an activity is updated, update changed properties
- DeleteActivity
- ...
"""
from src.handlers.actions.action import Action
from src.handlers.actions.create_activity import CreateActivity
from src.handlers.actions.update_activity import UpdateActivity
