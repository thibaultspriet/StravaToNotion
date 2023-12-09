"""Define types for object event sent by AWS Lambda runtime."""
from typing import Any, TypedDict


class Iam(TypedDict):
    """Type iam."""

    accessKey: str
    accountId: str
    callerId: str
    userArn: str
    userId: str


class Http(TypedDict):
    """Type http."""

    method: str
    path: str
    protocol: str
    sourceIp: str
    userAgent: str


class RequestContext(TypedDict):
    """Type request context."""

    accountId: str
    apiId: str
    authorizer: dict[str, Iam]
    domainName: str
    domainPrefix: str
    http: Http
    requestId: str
    routeKey: str
    stage: str
    time: str
    timeEpoch: int


class HttpEvent(TypedDict):
    """Type event."""

    version: str
    routeKey: str
    rawPath: str
    rawQueryString: str
    cookies: list[str]
    headers: dict[str, str]
    queryStringParameters: dict[str, str]
    requestContext: RequestContext
    body: str
    isBase64Encoded: bool


class SqsEvent(TypedDict):
    """Type of SQS event."""

    Records: list[dict[Any, Any]]
