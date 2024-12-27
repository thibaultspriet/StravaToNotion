"""Define constant values of the project."""
from string import Template
from typing import Literal

_allowed_keys = Literal[
    "id",
    "external_id",
    "upload_id",
    "athlete",
    "name",
    "distance",
    "moving_time",
    "elapsed_time",
    "total_elevation_gain",
    "elev_high",
    "elev_low",
    "sport_type",
    "start_date",
    "start_date_local",
    "timezone",
    "start_latlng",
    "end_latlng",
    "achievement_count",
    "kudos_count",
    "comment_count",
    "athlete_count",
    "photo_count",
    "total_photo_count",
    "map",
    "trainer",
    "commute",
    "manual",
    "private",
    "flagged",
    "workout_type",
    "upload_id_str",
    "average_speed",
    "max_speed",
    "has_kudoed",
    "hide_from_home",
    "gear_id",
    "kilojoules",
    "average_watts",
    "device_watts",
    "max_watts",
    "weighted_average_watts",
    "description",
    "photos",
    "gear",
    "calories",
    "segment_efforts",
    "device_name",
    "embed_token",
    "splits_metric",
    "splits_standard",
    "laps",
    "best_efforts",
]

STRAVA_ACTIVITY_FIELDS: list[_allowed_keys] = [
    "name",
    "external_id",
    "sport_type",
    "total_elevation_gain",
    "upload_id",
    "start_date",
    "id",
    "calories",
    "distance",
    "average_speed",
    "description",
    "max_speed",
    "moving_time",
]


NOTION_DATABASE_PROPERTIES_TEMPLATE = Template(
    """\
{
    "Name": {
        "title": [
            {
                "text": {
                    "content": "$name"
                }
            }
        ]
    },
    "Athlète": {
        "rich_text": [
            {
                "text": {
                    "content": "$username"
                }
            }
        ]
    },
    "Description": {
        "rich_text": [
            {
                "text": {
                    "content": "$description"
                }
            }
        ]
    },
    "Type": {
        "select": {
            "name": "$type"
        }
    },
    "Calories": { "number": $calories },
    "Start": {
      "date": {
        "start": "$start"
      }
    },
    "Activity ID": {
        "rich_text": [
            {
                "text": {
                    "content": "$activity_id"
                }
            }
        ]
    },
    "AVG Speed": { "number": $avg_speed },
    "Max Speed": { "number": $max_speed },
    "Total Elevation Gain": { "number": $total_elevation_gain },
    "External ID": {
        "rich_text": [
            {
                "text": {
                    "content": "$external_id"
                }
            }
        ]
    },
    "Upload ID": {
        "rich_text": [
            {
                "text": {
                    "content": "$upload_id"
                }
            }
        ]
    },
    "Time": { "number": $time },
    "Distance": { "number": $distance }
}
"""
)

NOTION_DATABASE_ACTIVITY_ID = "Activity ID"

NOTION_DATABASE_SCHEMA = {
    "External ID": {"rich_text": {}},
    "Type": {
        "select": {
            "options": [
                {"name": "Run", "color": "yellow"},
                {"name": "Ride", "color": "red"},
                {"name": "Swim", "color": "brown"},
                {"name": "VirtualRide", "color": "orange"},
            ]
        }
    },
    "Total Elevation Gain": {"number": {"format": "number"}},
    "Upload ID": {"rich_text": {}},
    "Start": {"date": {}},
    "Activity ID": {"rich_text": {}},
    "Calories": {"number": {"format": "number"}},
    "Distance": {"number": {"format": "number"}},
    "AVG Speed": {"number": {"format": "number"}},
    "Description": {"rich_text": {}},
    "Athlète": {"rich_text": {}},
    "Distance (km)": {"formula": {"expression": 'round(prop("Distance")/100)/10'}},
    "Max Speed": {"number": {"format": "number"}},
    "Time (min)": {"formula": {"expression": 'round(prop("Time")/60)'}},
    "Time": {"number": {"format": "number"}},
    "AVG Speed (km/h)": {"formula": {"expression": 'round(prop("AVG Speed")*3.6)'}},
    "Name": {"title": {}},
}
