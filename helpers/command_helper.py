#!/usr/bin/env python
"""This module contains code that helps generates the necessary queries that
modify data in the database"""
from datetime import datetime
from typing import Dict, List, TypeVar, Any, Iterable

from sqlalchemy.orm import Session
from sqlalchemy.orm import exc as orm_exc
from sqlalchemy_command_helper import command_helper
from helpers import query_helper
from helpers import id_helper

SessionType = TypeVar('SessionType', bound=Session)


def sanitize_data(fields: Iterable[str], data: Dict) -> Dict:
    """This function is used to remove any key value pairs in the dictionary
    used to create or update entities in the system

    Arg(s)
    ------
    fields -> The fields that are expected to be present in the dictionary
    data (dict) -> The dictionary whose value pairs will be removed if their key
        is not part of the list of fields to be returned

    Return(s)
    ---------
    tmp (dict) -> The new dictionary with the new key value pairs that match
        the models column
    """
    tmp = {}
    if 'token' in data:
        del data['token']

    for column in fields:
        if column in data:
            tmp[column] = data[column]
    return tmp


def save(
        session_obj: SessionType, model_cls, fields: Iterable[str],
        data: Dict, json_result: bool = False):
    """This function is responsible for storing a new instance of the model into
    the database

    Arg(s):
    -------
    session_obj -> object used to interact with the database
    model_cls -> class that represents the model that need to be saved in to
        the database
    fields(iterable[str]) -> list of fields that will be set on the model object
        saved to the database
    data (Dict) -> Dictionary that contains the fields (columns) and values that
        need to be set on the model before saving the model instance into the
        database
    json_result (bool) ->  indicates whether a json representation of the model
        instance that was just saved should be returned or the raw instance

    Return(s):
    ----------
    returns either a dictionary or instance of the model_cls depending on the
    value of json_result
    """
    clean_data = sanitize_data(fields, data)
    obj = model_cls()
    for field in fields:
        if field in clean_data:
            setattr(obj, field, clean_data[field])

    if 'ver' not in clean_data:
        setattr(obj, 'ver', id_helper.generate_id())

    session_obj.add(obj)
    if not json_result:
        return obj
    return obj.dict()


def update_by_id(
        session_obj, model_cls, _id: Any, data: Dict, json_result=False):

    """This function is responsible for updating a particular instance of a
    model when the id of that instance is known

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class that represents the model whose instance needs to be
        updated
    fields (Iterable[str]) -> list of fields that can be updated on the model
        before it's written to the database
    _id -> id of the instance of the model that needs to be updated
    data (dict) -> Dictionary that contains the fields that need to be updated
        and the values that they need to be set to
    json_result (bool) -> indicates whether the new state of the model's
        instance should be returned raw or converted to a dictionary

    Return(s)
    ---------
    returns a raw instance of the model or a dictionary representing the model
    """
    return update_by_params(
        session_obj, model_cls, [{"id": {"$eq": _id}}], data,
        json_result=json_result
    )


def update_by_params(
        session_obj: SessionType, model_cls,
        params: List[Dict], data, json_result=False):
    """This function is updates the instance of the model represented by the
    class in model_cls and identified by the arguments in the params parameter

    Arg(s)
    ------
    session_obj: the object used to interact with the database
    model_cls: class representing the model whose instance needs to be updated
    params (List[Dict]) -> parameters that will be used to identify the model
        instance that needs to be updated
    data (Dict) -> the fields that need to be updated with the values in the
        parameter
    json_result (bool) -> indicates whether the resulting instances of the model
        needs to be converted to a dictionary or the raw instance needs to be
        returned

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
    result = command_helper.update_by_params(
        session_obj, model_cls, query_helper.find_by_params,
        model_cls.COLUMNS, params, data
    )

    if json_result:
        return result.dict()

    return result


def delete_by_id(
        session_obj: SessionType, model_cls, _id,
        data: Dict = None, json_result=False):
    """This function is used to update an instance of the class indicated by
    id in _id

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class representing the model that needs to be updated
    _id -> id of the instance of the class that needs to be deleted
    data (Dict) -> other data that needs to be set of the object after it has
        been marked as deleted
    json_result (bool) -> indicates whether the deleted instance should be
        returned raw or converted to a dictionary

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
    return delete_by_params(
        session_obj, model_cls, [{'id': {'$eq': _id}}],
        data, json_result=json_result
    )


def delete_by_params(
        session_obj: SessionType, model_cls, params: List[Dict],
        data: Dict = None, json_result=False):
    """This function is used to update an instance of the class indicated by
    parameters in the params argument

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class representing the model that needs to be updated
    fields (Iterable[str]) -> list of fields that can be updated on the model
        before it's written to the database
    params (List[Dict]) -> parameters that can be used to identify the instance
        of the model to be deleted
    data (Dict) -> other data that needs to be set of the object after it has
        been marked as deleted
    json_result (bool) -> indicates whether the deleted instance should be
        returned raw or converted to a dictionary

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
    result = command_helper.delete_by_params(
        session_obj, model_cls,
        query_helper.find_by_params, model_cls.COLUMNS, params,
        data
    )

    if json_result:
        return result.dict()
    return result
