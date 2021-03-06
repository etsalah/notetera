#!/usr/bin/env python


def get_pagination_details(request_obj):
    """
    This function is used to get data sent with request that are used during
    pagination of data returned by endpoints that return a list of items.
    This function also provide default values for values that have been sent
    during the request

    Args:
    ~~~~~
        request_obj: request object that pagination data will be attached to

    Returns:
    ~~~~~~~~
        dict representing pagination information
    """

    params = get_json(request_obj)

    return {
        'id': params.get('id', ''),
        'limit': params.get('limit', 20),
        'sort': params.get('sort', []),
        'offset': params.get('offset', 0)
    }


def get_json(request_obj, remove_token=True):
    """
    This function is responsible for getting the json data that was sent with
    with a request or return an empty dict if no data is sent

    Args:
    ~~~~~
        request_obj: request object that data should be attached to

    Returns:
    ~~~~~~~~
        dict
    """
    result = {}
    if not hasattr(request_obj, 'json') or not request_obj.json:
        if hasattr(request_obj, 'params'):
            result = request_obj.params

    result = request_obj.json or {}

    if remove_token and 'token' in result:
        del result['token']

    return result
