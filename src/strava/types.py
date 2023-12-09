"""Define types of the Strava API."""
from typing import Literal, TypedDict


class MetaAthlete(TypedDict):
    """Type for MetaAthlete."""

    id: str


SportType = Literal[
    "AlpineSki",
    "BackcountrySki",
    "Badminton",
    "Canoeing",
    "Crossfit",
    "EBikeRide",
    "Elliptical",
    "EMountainBikeRide",
    "Golf",
    "GravelRide",
    "Handcycle",
    "HighIntensityIntervalTraining",
    "Hike",
    "IceSkate",
    "InlineSkate",
    "Kayaking",
    "Kitesurf",
    "MountainBikeRide",
    "NordicSki",
    "Pickleball",
    "Pilates",
    "Racquetball",
    "Ride",
    "RockClimbing",
    "RollerSki",
    "Rowing",
    "Run",
    "Sail",
    "Skateboard",
    "Snowboard",
    "Snowshoe",
    "Soccer",
    "Squash",
    "StairStepper",
    "StandUpPaddling",
    "Surfing",
    "Swim",
    "TableTennis",
    "Tennis",
    "TrailRun",
    "Velomobile",
    "VirtualRide",
    "VirtualRow",
    "VirtualRun",
    "Walk",
    "WeightTraining",
    "Wheelchair",
    "Windsurf",
    "Workout",
    "Yoga",
]


class PolylineMap(TypedDict):
    """Type for PolylineMap."""

    id: str
    polyline: str
    summary_polyline: str


class PhotosSummaryPrimary(TypedDict):
    """Type for PhotosSummary_primary."""

    id: int
    source: int
    unique_id: str
    urls: str


class PhotosSummary(TypedDict):
    """Type for PhotosSummary."""

    count: int
    primary: PhotosSummaryPrimary


class SummaryGear(TypedDict):
    """Type for SummaryGear."""

    id: str
    resource_state: int
    primary: bool
    name: str
    distance: float


class MetaActivity(TypedDict):
    """Type for MetaActivity."""

    id: int


class SummaryPRSegmentEffort(TypedDict):
    """Type for SummaryPRSegmentEffort."""

    pr_activity_id: int
    pr_elapsed_time: int
    pr_date: str
    effort_count: int


class SummarySegmentEffort(TypedDict):
    """Type for SummarySegmentEffort."""

    id: int
    activity_id: int
    elapsed_time: int
    start_date: str
    start_date_local: str
    distance: float
    is_kom: bool


class SummarySegment(TypedDict):
    """Type for SummarySegment."""

    id: int
    name: str
    activity_type: str
    distance: float
    average_grade: float
    maximum_grade: float
    elevation_high: float
    elevation_low: float
    start_latlng: list[float]
    end_latlng: list[float]
    climb_category: int
    city: str
    state: str
    country: str
    private: bool
    athlete_pr_effort: SummaryPRSegmentEffort
    athlete_segment_stats: SummarySegmentEffort


class DetailedSegmentEffort(TypedDict):
    """Type for DetailedSegmentEffort."""

    id: int
    activity_id: int
    elapsed_time: int
    start_date: str
    start_date_local: str
    distance: float
    is_kom: bool
    name: str
    activity: MetaActivity
    athlete: MetaAthlete
    moving_time: int
    start_index: int
    end_index: int
    average_cadence: float
    average_watts: float
    device_watts: bool
    average_heartrate: float
    max_heartrate: float
    segment: SummarySegment
    kom_rank: int
    pr_rank: int
    hidden: bool


class Split(TypedDict):
    """Type for Split."""

    average_speed: float
    distance: float
    elapsed_time: int
    elevation_difference: float
    pace_zone: int
    moving_time: int
    split: int


class Lap(TypedDict):
    """Type for Lap."""

    id: int
    activity: MetaActivity
    athlete: MetaAthlete
    average_cadence: float
    average_speed: float
    distance: float
    elapsed_time: int
    start_index: int
    end_index: int
    lap_index: int
    max_speed: float
    moving_time: int
    name: str
    pace_zone: int
    split: int
    start_date: str
    start_date_local: str
    total_elevation_gain: float


class DetailedActivity(TypedDict):
    """Type for DetailedActivity."""

    id: int
    external_id: str
    upload_id: str
    athlete: MetaAthlete
    name: str
    distance: float
    moving_time: int
    elapsed_time: int
    total_elevation_gain: float
    elev_high: float
    elev_low: float
    sport_type: SportType
    start_date: str
    start_date_local: str
    timezone: str
    start_latlng: list[float]
    end_latlng: list[float]
    achievement_count: int
    kudos_count: int
    comment_count: int
    athlete_count: int
    photo_count: int
    total_photo_count: int
    map: PolylineMap
    trainer: bool
    commute: bool
    manual: bool
    private: bool
    flagged: bool
    workout_type: int
    upload_id_str: str
    average_speed: float
    max_speed: float
    has_kudoed: bool
    hide_from_home: bool
    gear_id: str
    kilojoules: float
    average_watts: float
    device_watts: bool
    max_watts: int
    weighted_average_watts: int
    description: str
    photos: PhotosSummary
    gear: SummaryGear
    calories: float
    segment_efforts: list[DetailedSegmentEffort]
    device_name: str
    embed_token: str
    splits_metric: Split
    splits_standard: Split
    laps: list[Lap]
    best_efforts: DetailedSegmentEffort
