"""Define handlers for Strava subscriptions."""


def callback_validation(
    query_parameters: dict[str, str], verify_token: str
) -> dict[str, str]:
    """
    Validate the Strava subscription creation.

    When we register a callback for Strava application, Strava issues a GET request to which the callback must
    respond with { “hub.challenge”: ”XXX” } where XXX is the value of the parameter hub.challenge sent by Strava

    :param query_parameters: parameters sent by Strava (hub.mode ; hub.challenge ; hub.verify_token )
    :param verify_token: the initial verify token. Used to verify that the Strava request is correct.
    :return: dictionary with key hub.challenge and value is the one sent by Strava.
    """
    if verify_token != query_parameters["hub.verify_token"]:
        raise RuntimeError(
            f"hub.verify token incorrect, value received : {query_parameters['hub.verify_token']}"
        )
    return {"hub.challenge": query_parameters["hub.challenge"]}
