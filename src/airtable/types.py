"""Define types proper to airtable API."""
from typing import Literal, Optional, TypedDict


class Sort(TypedDict):
    """Type for sort values."""

    field: str
    direction: Optional[Literal["asc", "desc"]]


class ListRecordsQueryParameters(TypedDict):
    """Type for query parameters of list records endpoint."""

    timeZone: Optional[str]
    userLocale: Optional[str]
    pageSize: Optional[int]
    maxRecords: Optional[int]
    offset: Optional[str]
    view: Optional[str]
    sort: Optional[list[Sort]]
    filterByFormula: Optional[str]
    cellFormat: Optional[Literal["json", "string"]]
    fields: Optional[list[str]]
    returnFieldsByFieldId: Optional[bool]
    recordMetadata: Optional[list[int]]


class UpdateRecordBodyParameters(TypedDict):
    """Type for body parameters of update record endpoint."""

    fields: dict
    returnFieldsByFieldId: Optional[bool]
    typecast: Optional[bool]


class CreateRecordsBodyParameter(TypedDict):
    """Type for body parameters of the create records endpoint."""

    fields: Optional[dict]  # To create a single record
    records: Optional[list[dict]]
    returnFieldsByFieldId: Optional[bool]
    typecast: Optional[bool]


class Record(TypedDict):
    """Type for a record."""

    id: str
    createdTime: str
    fields: dict
    commentCount: Optional[int]
