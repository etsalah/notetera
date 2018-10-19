#!/usr/bin/env python
"""This module contains code that helps generates the necessary queries that
read data from the database"""
from typing import Dict, List, TypeVar

from sqlalchemy_query_helper import query_helper
from sqlalchemy.orm import Session

SessionType = TypeVar('SessionType', bound=Session)
SUPPORTED_QUERY_OPERATORS = (
    '$ne', '$eq', '$in', '$nin', '$gt', '$gte', '$lt', '$lte'
)


def query(
        session_obj: SessionType, model_cls,
        params: List[Dict], pagination_args: Dict, json_result=False):
    """This function is responsible for returning a filter list of model
    instances from the database.

    Arg(s):
    -------
    session_obj (SessionType) -> The object used to interact with the data model
    model_cls -> Model class that represents the database table to get data from
    params (List[Dict]) -> The list of filter condictions that will be used to
        filter the data that is returned
    pagination_args (Dict) -> The paginations arguments that indicates how many
        entities to be returned from the database and how many records to be
        skipped
    json_result (bool) -> indicates whether the data returned is a list of model
        instances or a list of dictionaries representing each model instance
        that is returned which

    Return(s):
    ----------
        returns a list of instance of class passed in the model_cls param or
        list of dictionaries representing
    """
    result = query_helper.query(session_obj, model_cls, params, pagination_args)
    if not json_result:
        return result

    return [row.dict() for row in result]


def find_by_id(session_obj: SessionType, model_cls, _id, json_result=False):
    """This function is responsible for finding the instance of the model that
    is identified by value in the _id argument

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class representing instance of the model to be found
    _id -> id of the model to be found
    json_result -> indicates whether the found object used b returned as a
        dictionary or a raw instance

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
    return find_by_params(
        session_obj, model_cls, [{"id": {"$eq": _id}}], json_result)


def find_by_params(
        session_obj: SessionType, model_cls, params: List[Dict],
        json_result=False):
    """This function is responsible for finding the instance of the model that
    is identified by filter parameters in params

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class representing instance of the model to be found
    params -> list of parameters to find a instance of the model class by
    json_result -> indicates whether the found object used b returned as a
        dictionary or a raw instance

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
    result = list_query(
        session_obj, model_cls, params, {"offset": 0, "limit": 1}, json_result)
    for row in result:
        return row


def list_query(
        session_obj: SessionType, model_cls, params: List[Dict]=None,
        pagination_args: Dict=None, json_result=False):
    """This function is responsible for returning a list of model instances

    Arg(s):
    -------
    session_obj -> object used to interact with the database
    model_cls -> class that represents the model instances to be returned
    params (List[Dict]) -> List of parameters to used to filter the instances of
        model class instances to be returned
    pagination_args (Dict) -> parameter that indicate how many matched instances
        of the model classes to return and how many matched instances of the
        model classes to skip

    Return(s):
    ---------
    List of model class instances either a raw class instances or as a list of
    dictionaries
    """
    return query(session_obj, model_cls, params, pagination_args, json_result)


def count(session_obj: SessionType, model_cls, params: List[Dict] = None):
    """This function is responsible for returning a count of rows of a model 
    that match a particular 
    
    Args:
        session_obj: object used to interact with the database
        model_cls: the class of the model whose records are to be counted
        params: list of parameters that need to be counted
    """
    return query_helper.count(session_obj, model_cls, params)
